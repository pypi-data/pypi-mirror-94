import uuid, json

from rest_framework.response import Response
from .models import IdentityKey, SignedPreKey, PreKey, EncryptingSenderKey, DecryptingSenderKey, Party
from django.db.models import Q
from firebase_admin import db
from django.conf import settings

DEFAULT_APP = settings.DEFAULT_APP
FIREBASE_REF = settings.FIREBASE_REF
FIREBASE_REF_DEV = settings.FIREBASE_REF_DEV



class StickProtocol():

    def __init__(self, UserModel, GroupModel):
        self.User = UserModel
        self.Group = GroupModel


    def process_pre_key_bundle(self, request, user):
        """
        A user must upload their PreKeyBundle at registration time. Before uploading their PreKeyBundle, they need to verify
        their phone number, and get their LimitedAccessToken.
        """
        data = request.data
        identityKey = data["identityKey"]
        signedPreKey = data["signedPreKey"]
        preKeys = data["preKeys"]
        IdentityKey.objects.create(public=identityKey['public'], localId=identityKey['localId'], deviceId=0, user=user,
                                   cipher=identityKey['cipher'], salt=identityKey['salt'])
        SignedPreKey.objects.create(public=signedPreKey['public'], signature=signedPreKey["signature"],
                                    keyId=signedPreKey['id'], user=user, cipher=signedPreKey['cipher'],
                                    salt=signedPreKey['salt'])
        for preKey in preKeys:
            PreKey.objects.create(public=preKey['public'], keyId=preKey["id"], user=user, cipher=preKey['cipher'],
                                  salt=preKey['salt'])
        user.set_password(data["password"])
        user.oneTimeId = data["oneTimeId"]
        user.nextPreKeyId = data['nextPreKeyId']
        user.finishedRegistration = True
        user.save()
        Party.objects.create(user=user)
        # LimitedAccessToken.objects.get(phone=request.data['phone']).delete()



    def process_pre_keys(self, request):
        """
        A user would need to refill their PreKeys on the server every while whenever it goes below a certain N value.
        This method save preKeys and updates the nextPreKeyId value
        """
        user = request.user
        preKeys = request.data['preKeys']
        for preKey in preKeys:
            PreKey.objects.create(public=preKey['public'], keyId=preKey["id"], user=user, cipher=preKey['cipher'],
                                  salt=preKey['salt'])
        user.nextPreKeyId = request.data['nextPreKeyId']
        user.save()



    def get_pre_key_bundle(self, request, user_id):
        """
        The following get method is used to fetch the PreKeyBundle of user to create a pairwise signal session. The request must contain
        a boolean `isSticky` to know whether this bundle would be used to communicate a SenderKey or not. If it will be used to
        communicate a SenderKey, then the PreKey must be marked as used, otherwise the PreKey is deleted from the server.
        """
        # id = request.GET.get("id")
        deviceId = int(request.GET.get("deviceId"))
        if request.GET.get('isSticky') == None or json.loads(request.GET.get('isSticky')):
            isSticky = True
        else:
            isSticky = False
        user = self.User.objects.get(id=user_id)
        identityKey = IdentityKey.objects.get(user=user)
        signedPreKey = SignedPreKey.objects.get(user=user)
        preKey = PreKey.objects.filter(user=user, used=False).first()
        oneTimeId = user.oneTimeId
        PKB = {
            "identityKey": identityKey.public,
            "localId": identityKey.localId,
            "userId": id,
            "deviceId": deviceId,
            "signedPreKey": signedPreKey.public,
            "signedPreKeyId": signedPreKey.keyId,
            "signature": signedPreKey.signature,
            "preKey": preKey.public,
            "preKeyId": preKey.keyId,
            "oneTimeId": oneTimeId,
            "phone": user.phone
        }
        if not isSticky:
            preKey.delete()
        else:
            preKey.used = True
            preKey.save()
        return PKB




    def get_pre_key_bundles(self, request, users_id):
        """
        Similar to the above method, but fetches PreKeyBundles of several users at once. This method allows a user to
        communicate their SenderKey to multiple members of a party at once.
        """
        # You can either provide in the request a list of `users_id` or just a `group_id`.
        # if "users_id" in request.data:
        #     users_id = request.data["users_id"]
        # else:
        #     users_id = Group.objects.get(id=request.data["group_id"]).get_all_users_ids()

        bundles = {}
        # Make sure the current user is the first in the list. When creating DecryptingSenderKeys client-side to share
        # with other members, their must already be a corresponding EncryptingSenderKey.
        if request.user.id in users_id:
            users_id.remove(request.user.id)
            users_id.insert(0, request.user.id)

        toBeRemoved = []
        for id in users_id:
            # If a non-existent user_id was provided, then their id must be removed from the list
            try:
                identityKey = IdentityKey.objects.get(user__id=id)
            except:
                toBeRemoved.append(id)
                continue
            signedPreKey = SignedPreKey.objects.get(user__id=id)
            preKey = PreKey.objects.filter(user__id=id, used=False).first()
            oneTimeId = self.User.objects.get(id=id).oneTimeId
            PKB = {
                "identityKey": identityKey.public,
                "localId": identityKey.localId,
                "userId": id,
                "deviceId": 1,
                "signedPreKey": signedPreKey.public,
                "signedPreKeyId": signedPreKey.keyId,
                "signature": signedPreKey.signature,
                "preKey": preKey.public,
                "preKeyId": preKey.keyId,
                "oneTimeId": oneTimeId
            }
            preKey.used = True
            preKey.save()
            bundles[id] = PKB
        for id in toBeRemoved:
            users_id.remove(id)
        dict = {"bundles": bundles, "users_id": users_id}
        return dict



    def get_sender_key(self, request):
        """
        This method is used to fetch the SenderKey of a stickySession.
        The body should contain the following fields:
            * stickId - String
            * memberId - String
            * isSticky - Boolean (are you fetching the SenderKey of a Sticky session or a standard session)
            * isInvitation - Boolean
        """
        memberId = request.data['memberId']
        stickId = request.data['stickId']
        isSticky = request.data['isSticky']
        user = request.user
        isInvitation = False
        if 'isInvitation' in request.data:
            isInvitation = request.data['isInvitation']
        member = self.User.objects.get(id=memberId)

        # You need to check whether the user is authorized to fetch that SenderKey
        authorized = False
        if user in member.blocked.all(): # A blocked user is not authorized
            return {'authorized': authorized}
        if isInvitation: # An invited user is authorized
            group = self.Group.objects.get(id=stickId[:36])
            if group in user.invited_groups.all():
                authorized = True
        elif stickId.startswith(user.party.id): # A user is authorized to fetch SenderKeys of their own profile (user.party.id)
            authorized = True
        else:
            groupId = stickId[:36] if isSticky else request.data['groupId']
            group = self.Group.objects.filter(id=groupId).first()
            if group:
                if group in user.groups.all(): # A group member is authorized
                    authorized = True
            else:
                party = Party.objects.get(id=stickId[:36])
                # A user connected with another user should be authorized
                if party.user and (user in party.user.connections.all() or user.phone in party.user.contacts):
                    authorized = True
                else:
                    if user in party.connections.all(): # A user in the connections list of a party should be authorized
                        authorized = True
                    else:
                        userGroups = user.groups.all()
                        for group in party.groups.all():
                            if group in userGroups: # If a Party and a User have a mutual Group, then that user is authorized
                                authorized = True
                                break
        if not authorized: # if NOT authorized, return 401
            return {'authorized': authorized}

        if isSticky: # Fetching the SenderKey of a sticky session
            if memberId != user.id: # Trying to fetch DSK
                senderKey = DecryptingSenderKey.objects.filter(stickId=stickId, ofUser=memberId,
                                                           forUser=user).first()
            else: # Trying to fetch ESK
                partyId = stickId[:36]
                chainId = stickId[36:]
                senderKey = EncryptingSenderKey.objects.filter(partyId=partyId, chainId=chainId, user=user).first()
        else: # Trying to fetch DSK of a standard group session
            oneTimeId = request.data['oneTimeId']
            senderKey = DecryptingSenderKey.objects.filter(stickId=stickId, ofOneTimeId=oneTimeId,
                                                           forOneTimeId=user.oneTimeId).first()
        key = None
        if senderKey: # If the SenderKey exists, we will return it
            if memberId != user.id:
                key = senderKey.key
            else:
                key = {'id': senderKey.keyId, 'chainKey': senderKey.chainKey, 'public': senderKey.public,
                       'cipher': senderKey.cipher, 'step': senderKey.step}
        # SenderKey does not exist, send a `PendingKey` request to the target user to upload their key,
        # through a realtime database.
        else:
            if isSticky:
                phone = self.User.objects.get(id=memberId).phone
            else:
                phone = request.data['phone']
            dev = request.data['dev']
            firebase_ref = FIREBASE_REF_DEV if dev else FIREBASE_REF
            ref = db.reference('users/' + phone + '/pendingKeys/', DEFAULT_APP, firebase_ref)
            ref.update({stickId + '--' + str(user.id): user.phone})
        return {'authorized': authorized, 'senderKey': key}



    def get_standard_sender_keys(self, request, group):
        """
        This method is used to fetch the standard session sender keys of a group.
        """
        stickId = request.data['chatId']
        keysToFetch = request.data['keysToFetch']
        if group not in request.user.groups.all():
            return {'authorized': False}
        senderKeys = {}
        for id in keysToFetch:
            senderKey = DecryptingSenderKey.objects.filter(stickId=stickId, ofOneTimeId=id,
                                                           forOneTimeId=request.user.oneTimeId).first()
            key = None
            if senderKey:
                key = senderKey.key
            senderKeys[id] = key
        return {'authorized': True, 'senderKeys': senderKeys}



    def get_uploaded_sender_keys(self, request):
        """
        Before a user makes an upload they need to know which stickId to use (whether the current sticky session has expired).
        Also, they need to know which members of the target party does not have their SenderKey for that sticky session.
        This following method expects these arguments in the request body:
        * groups_ids - a list of groups ids
        * connections_ids - a list of users ids
        * isSticky - boolean, indicates whether the user is intending to use a sticky session
        * isProfile - boolean, indicates whether the user is sharing to their profile (includes all their connections)
        * partyId (optional) - boolean, the partyId of a user
        """
        groups_ids = request.data['groups_ids']
        connections_ids = request.data['connections_ids']
        isSticky = request.data['isSticky']
        isProfile = False
        if 'isProfile' in request.data:
            isProfile = request.data['isProfile']
        membersIds = []
        if not isProfile and 'partyId' not in request.data:
            if len(groups_ids) == 1 and len(connections_ids) == 0: # Sharing with a single group
                if isSticky: # Using sticky session
                    membersIds = self.Group.objects.get(id=groups_ids[0]).get_members_ids()
                    partyId = groups_ids[0]
                else: # Using standard session
                    membersIds = self.Group.objects.get(id=groups_ids[0]).get_members_otids()
                    partyId = request.data["chatId"]
            else: # Sharing with a collection of groups and/or users
                if len(groups_ids) > 0 and len(connections_ids) > 0:
                    party = Party.objects.filter(Q(groups=groups_ids) & Q(connections=connections_ids)).first()
                elif len(groups_ids) > 0:
                    party = Party.objects.filter(Q(groups=groups_ids) & Q(connections=None)).first()
                else:
                    connections_ids.append(request.user.id)
                    party = Party.objects.filter(Q(groups=None) & Q(connections=connections_ids)).first()
                if party == None: # Create a new Party object if does not exist
                    party = Party.objects.create()
                    party.groups.set(groups_ids)
                    party.connections.set(connections_ids)
                for group_id in groups_ids:
                    group = self.Group.objects.get(id=group_id)
                    for memberId in group.get_members_ids():
                        if not memberId in membersIds:
                            membersIds.append(memberId)
                for connection_id in connections_ids:
                    if not connection_id in membersIds:
                        membersIds.append(connection_id)
                if request.user.id not in membersIds:
                    membersIds.append(request.user.id)
                partyId = party.id
        elif 'partyId' in request.data: # Sharing to the party of a user
            membersIds = [request.user.id]
            if not (len(groups_ids) == 1 and len(connections_ids) == 0):
                party = Party.objects.get(id=request.data['partyId'])
                if party.user and party.user.id != request.user.id:
                    membersIds.append(party.user.id)
            partyId = request.data['partyId']
        else: # Sharing to the currentUser's party (currentUsers' profile)
            membersIds = connections_ids
            partyId = Party.objects.get(user=request.user).id
        dict = {}
        bundlesToFetch = []
        responseDict = {}

        # Find the right stickId
        chainId = 0
        senderKeys = EncryptingSenderKey.objects.filter(partyId=partyId, user=request.user).order_by('-chainId')
        if len(senderKeys) > 0:
            activeSenderKey = senderKeys[0]
            if not isSticky: # A standard session is valid
                dict[request.user.id] = {'exists': True}
            elif activeSenderKey.step < 100: # Check whether is sticky session has not expired
                chainId = activeSenderKey.chainId
                dict[request.user.id] = {'exists': True}
                responseDict["step"] = activeSenderKey.step
            else: # Sticky session has expired, increment chainId by 1
                chainId = int(activeSenderKey.chainId) + 1
                dict[request.user.id] = {'exists': False}
                bundlesToFetch.append(request.user.id)
        else:
            dict[request.user.id] = {'exists': False}
        stickId = str(partyId) + str(chainId)
        if not isSticky:
            stickId = partyId

        for memberId in membersIds: # loop of the target users and check if they have their SenderKey
            if isSticky:
                if request.user.id != memberId:
                    senderKey = DecryptingSenderKey.objects.filter(stickId=stickId, ofUser=request.user,
                                                                   forUser=memberId).first()
                else:
                    senderKey = EncryptingSenderKey.objects.filter(partyId=partyId, chainId=chainId,
                                                                   user=request.user).first()
            else:
                senderKey = DecryptingSenderKey.objects.filter(stickId=stickId, ofOneTimeId=request.user.oneTimeId,
                                                               forOneTimeId=memberId).first()
            if senderKey:
                response = {'exists': True}
            else:
                response = {'exists': False}
                bundlesToFetch.append(memberId)
            dict[memberId] = response
        responseDict["stickId"] = stickId
        responseDict["partyId"] = partyId
        responseDict["members"] = dict
        if request.user.id in bundlesToFetch:
            bundlesToFetch.remove(request.user.id)
            bundlesToFetch.insert(0, request.user.id)
        responseDict["bundlesToFetch"] = bundlesToFetch
        return responseDict



    def get_stick_id(self, request):
        """
        This method gets the active sticky session stickId associated with a particular partyId that already exists, and
        its current step.
        """
        partyId = request.data['partyId']
        senderKeys = EncryptingSenderKey.objects.filter(partyId=partyId, user=request.user).reverse()
        activeSenderKey = senderKeys[0]
        responseDict = {}
        if activeSenderKey.step < 100:
            chainId = activeSenderKey.chainId
            responseDict['step'] = activeSenderKey.step
        else:
            chainId = int(activeSenderKey.chainId) + 1
        responseDict['stickId'] = str(partyId) + str(chainId)
        return responseDict


    def process_sender_key(self, request):
        """
        This method is used to save a SenderKey of a sticky session for a user. Typically used when a user
        receives a `PendingKey` request.
        """
        decryptingSenderKey = DecryptingSenderKey.objects.create(key=request.data['key'],
                                                                 stickId=request.data['stickId'], ofUser=request.user)
        preKey = PreKey.objects.get(keyId=request.data['preKeyId'], user__id=request.data['forUser'])
        decryptingSenderKey.preKey = preKey
        forUser = self.User.objects.get(id=request.data['forUser'])
        decryptingSenderKey.forUser = forUser
        decryptingSenderKey.save()



    def process_sender_keys(self, request):
        """
        This method is used to save SenderKeys of multiple users at once. Before making an upload, and after
        the user has made a request to get the UploadedSenderKeys, and now knows which users does not have SenderKeys for
        a particular sticky session, the user can upload those SenderKeys through this method.
        """
        users_id = request.data['users_id']
        keys = request.data['keys']
        for id in users_id:
            data = keys[id]
            preKey = PreKey.objects.get(keyId=data['preKeyId'], user__id=id)
            if id != request.user.id: # Other user? Create a DSK
                forUser = self.User.objects.get(id=data['forUser'])
                DecryptingSenderKey.objects.create(key=data['key'],
                                                   stickId=data['stickId'], ofUser=request.user,
                                                   preKey=preKey, forUser=forUser)
            else: # Current user? Create an ESK
                partyId = data['stickId'][:36]
                chainId = data['stickId'][36:]
                EncryptingSenderKey.objects.create(keyId=data['id'], preKey=preKey,
                                                   partyId=partyId, chainId=chainId,
                                                   user=request.user, chainKey=data['chainKey'],
                                                   public=data['public'],
                                                   cipher=data['cipher'])
        if "group_id" in request.data:
            request.user.just_added_groups.remove(request.data["group_id"])


    def process_standard_sender_keys(self, request):
        """
        This method is used to upload the SenderKeys of a standard session.
        """
        stickId = request.data['chatId']
        keysToUpload = request.data['keysToUpload']
        for oneTimeId, senderKey in keysToUpload.items():
            DecryptingSenderKey.objects.create(key=senderKey, stickId=stickId, ofUser=request.user,
                                               forOneTimeId=oneTimeId, ofOneTimeId=request.user.oneTimeId)


    def verify_password_and_get_keys(self, request, user):
        """
        This Login method should be called after the user have verified their phone number and got their LimitedAccessToken.
        As a 2FA mechanism, the user need to provide their password. If the password is correct, return to the user their keys:
            * Identity Key
            * Signed Pre Key
            * Pre Keys
            * Encrypting Sender Keys
        On the client-side, the password will be used to decrypt the private keys of the IdentityKey, SignedPreKey
        and PreKeys (using a secret key derived from the password through Argon2).
        The user will be able to re-establish their pairwise signal sessions. After that, the user can decrypt their ESKs
        as well as any of the DSKs the was sent to them, which they can fetch again from the server as needed.
        """
        # user = self.User.objects.get(phone=request.data['phone'])
        if user.check_password(request.data['password']):
            identityKey = IdentityKey.objects.get(user=user)
            signedPreKey = SignedPreKey.objects.get(user=user)
            preKeysList = PreKey.objects.filter(user=user)
            senderKeysList = EncryptingSenderKey.objects.filter(user=user)
            bundle = {
                "identityPublic": identityKey.public,
                "identityCipher": identityKey.cipher,
                "identitySalt": identityKey.salt,
                "localId": identityKey.localId,
                "userId": user.id,
                "deviceId": 0,
                "signedPublic": signedPreKey.public,
                "signedCipher": signedPreKey.cipher,
                "signedSalt": signedPreKey.salt,
                "signedPreKeyId": signedPreKey.keyId,
                "signature": signedPreKey.signature,
            }
            preKeys = []
            for preKey in preKeysList:
                key = {'id': preKey.keyId, 'public': preKey.public, 'cipher': preKey.cipher, 'salt': preKey.salt}
                preKeys.append(key)
            bundle['preKeys'] = preKeys
            senderKeys = []
            for senderKey in senderKeysList:
                stickId = senderKey.partyId + senderKey.chainId
                key = {'id': senderKey.keyId, 'chainKey': senderKey.chainKey, 'public': senderKey.public,
                       'cipher': senderKey.cipher, 'stickId': stickId, 'step': senderKey.step}
                senderKeys.append(key)
            bundle['senderKeys'] = senderKeys
            user.oneTimeId = uuid.uuid4()
            user.save()
            # LimitedAccessToken.objects.get(phone=request.data['phone']).delete()
            return {"bundle": bundle, "success": True}
        else:
            return Response({"success": False})



    # def get_one_time_id(self, request):
    #     """
    #     This method is used to fetch the OneTimeId of a user.
    #     An example of usage is when entering a chat room a user need to know
    #     the current oneTimeId of the recipient.
    #     """
    #     id = request.GET.get("id")
    #     user = User.objects.get(id=id)
    #     return Response({"oneTimeId": user.oneTimeId})
