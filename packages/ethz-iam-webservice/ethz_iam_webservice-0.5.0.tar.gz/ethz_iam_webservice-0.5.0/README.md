# ETHZ IAM Webservice

Manage users, groups and services of the ETH Identity and Access Management system (IAM)

## Command Line Interface

When installing this module, the `iam` command is also installed. The **basic parameters which are always needed** – otherwise they will be asked interactivley – are:

```bash
$ iam -u admin-username --password MY-SECRET-PASSWORD
```

You can also set these environment variables instead:

```bash
$ export IAM_USERNAME=admin-username
$ export IAM_PASSWORD=MY-SECRET-PASSWORD
```


**Group**

```bash
$ iam group <group-name> -i / --info
$ iam group <group-name> -m / --members
$ iam group <group-name> -d / --delete 

$ iam group <group-name> -a user1 --add user2
$ iam group <group-name> -r user3 --remove user4
```

**User**

Get info about a user, as well as granting/revoking a service or setting its password:

```bash
$ iam user username
$ iam user username --grant-service LDAPS, -g Mailbox
$ iam user username --revoke-service LDAPS, -r Mailbox
$ iam user username --set-password [-s LDAPS [-s Mailbox]] [--service-password $trengGehe1m]
```

**Person**

Get info about a person (identity) and its users. You might either provide a username, a NPID or a email address.

```bash
$ iam person username
$ iam person some.person@ethz.ch
$ iam person 123445
```


## Synopsis

### Login
```
import ethz_iam_webservice
import getpass

e = ethz_iam_webservice.login('admin4iam', getpass.getpass())
```

### Person
```
person = e.get_person('name@example.com')
person = e.get_person('some_username')
person = e.get_person(123456)             # npid (internal Person identifier)

person.usernames                          # an array of dicts of usernames
person.data                               # raw webservice response
person.firstname
person.familyname
person.email
# etc.
```

### User and Services

```
user = person.new_user('username', 'password', 'description')
user = e.get_user('username')
user.services                             # an array of dicts of services

user.grant_service("LDAPS")
user.grant_service("Active Directory")
user.grant_service("Mailbox")
user.grant_service("WLAN_VPN")

user.revoke_service("LDAPS")

user.delete() 
user.add_to_group('groupname')
user.remove_from_group('groupname')
```

**Mailbox Service**

```
# get service information
gs = user.get_service("Mailbox")

# all attributes of the granted Mailbox service
gs.data
{
  "sn": "Lastname",
  "givenName": "Firstname",
  "displayName": "neumond",
  "description": "this acccount is for creating moons",
  "mail": "neumond@ethz.ch",
  "isHidden": "false",
  "noMailReceive": "false",
  "quota": "5GB",
  "homeDrive": null,
  "homeDirectory": "\\\\\\\\d.ethz.ch\\\\users\\\\all\\\\neumond",
  "profilePath": "\\\\\\\\d.ethz.ch\\\\users\\\\all\\\\neumond\\\\%pafs",
  "unixHomeDirectory": "unixHomeDirectory",
  "loginShell": "/bin/bash",
  "primaryGroup": "Domain Users",
  "unifiedMessagingTask": null,
  "telephoneNumber": null,
  "proxyAddresses": [
    "SMTP:neumond@ethz.ch",
    "smtp:neumond@intern.ethz.ch"
  ]
}

# set a email-forward, description
gs.forward_address = 'neumond@example.com'
gs.description = 'some new description'
gs.save()
```

### Group and Group Members

**get single group** - returns a Group object or throws a ValueError if group is not found

```
group = e.new_group(
    name        = 'group-name',
    description = 'something meaningful',
    admingroup  = 'ID SIS',              # responsible admin group
    targets     = ['AD', 'LDAPS'],       # please specify at least one target system
    members     = ['user1', 'user2']
)

group = e.get_group('groupname')
group = e.get_group(123456)              # gidNumber
group.data                               # all data received from webservice
group.members                            # returns array of usernames or group-names
group.gidNumber
group.<attribute>
```

**add/remove group members**

```
group.add_members('some', 'new', 'members')
group.set_members('just', 'these')
group.del_members('remove', 'these', 'members')
```

**search for groups** - Result is always a list of groups or an empty list

```
groups = e.get_groups(agroup='ID SIS')
groups = e.get_groups(name='starts_with*')
groups = e.get_groups(agroup='ID SIS', name='starts_with*')
```

### Mailinglists

```
ml = e.get_mailinglist('ID.SIS.SSDM')
ml = e.get_mailinglist('sis@id.ethz.ch')
ml.name
ml.mail
ml.gidNumber
ml.groupType
ml.displayName
...

ml.members        # returns all (direct) members of that list
ml.add_members('user1', 'user2')
ml.del_members('user3, 'user4')
```

See also [FAQ](https://gitlab.ethz.ch/vermeul/ethz-iam-webservice/-/wikis/FAQ)
