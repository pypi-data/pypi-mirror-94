Viel info in:

- Message-ID: <e961a240f7404dfaae066271ec6011e1@kit-msx-32.kit.edu>
- https://git.scc.kit.edu/simon/reg-app/blob/branch-2.6/bwreg-webapp/src/main/java/edu/kit/scc/webreg/rest/ExternalUserController.java#L33

# external-user
## create

external-user/create -H "Content-Type: application/json"     -X POST -d '{"externalId":"test0002"}'    

## update

external-user/update -X POST -d '...'

## find

external-user/find/attribute/urn:oid:0.9.2342.19200300.100.1.1/hdf_neewmarcus
external-user/find/externalId/%22hdf_61230996-664f-4422-9caa-76cf086f0d6c@unity-hdf%22
extrenal-user/find/all

## activate:

external-user/activate/externalId/<externalId>

## deactivate:

external-user/deactivate/externalId<externalId>


# external-reg
https://git.scc.kit.edu/simon/reg-app/-/blob/branch-2.6/bwreg-webapp/src/main/java/edu/kit/scc/webreg/rest/ExternalRegistryController.java
## register

external-reg/register/externalId/<externalId>/ssn/<serviceId>
serviceId = "sshtest"

## find

external-reg/find/externalId/<externalId>


## deregister

external-reg/deregister/externalId/<externalId>/ssn/<serviceId>


# group-admin

## find

Gibt rudimentäre Infos über die Gruppe aus:
group-admin/find/id/<id>
group-admin/find/name/<name>

group-admin/find/name/mytestcollab
group-admin/find/id/1009662

## find-detail

Gibt genauere Infos raus. Z.B. auch die Member und übergeordnete Gruppen:
group-admin/find-detail/id/<id>
group-admin/find-detail/name/<name>

## create 

Legt eine Gruppe an:
group-admin/create/<ssn>/<name>
<ssn> - Der Service Short Name, des Dienstes, dem die Gruppe zugeordnet ist.

## add 

Fügt ein Benutzer einer Gruppe dazu, oder nimmt ihn raus:
group-admin/add/groupId/<groupId>/userId/<userId>

## remove 

group-admin/remove/groupId/<groupId>/userId/<userId>

<userId> - Datenbank Id des Benutzers
<groupId> - Datenbank Id der Gruppe

