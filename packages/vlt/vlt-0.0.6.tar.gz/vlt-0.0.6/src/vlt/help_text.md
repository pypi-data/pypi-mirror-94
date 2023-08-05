
help menu
=========

`vlt <CMD> <ARGS/KWARGS>`

CMD     command flag

ARGS/   commands for static mode. kwargs are
KWARGS  derived from arg list by <-> demarcation. I.E.

`<CMD> arg_one -key_one value_one arg_two`

static mode
===========

CMD
---

- `[-a, +, add]` - add entry to db
- `[-ar, archive]` - move db to archives
- `[-c, consume]` - consume csv file to db
- `[-d, dump]` - dump db contents to an unencrypted csv file
- `[-e, edit]` - edit db entry
- `[-ex, exp, export]` - export db to local directory
- `[-g, get]` - get entry from db
- `[-h, --help]` - help menu
- `[-l, lnk, link]` - link vlt to external db file
- `[-ls, ls, list]` - list current/archived db's
- `[-m, mk, make]` - make entry with vlt generated password
- `[-rm, rm, -, remove]` - remove entry from db
- `[-rs, reset]` - reset key or table
- `[-s, set, settings]` - set settings   
- `[ipython]` - open ipython terminal with `self` in scope
                                
**note** ipython is not a listed vlt requirement, must have previously installed

command options
---------------

### `[add/edit/get/remove]`

#### KWARGS
- `[-i] <INDEX>` - relative index of entry to select
- `[-s] <SOURCE>` - source to search against in db
- `[-u] <USERNAME>` - username to search against in db
- `[-p] <PASSWORD>` - password to search against in db       
        
### `[archive]`

#### ARGS
- `<FILENAME>` - filename for archived db

#### KWARGS
- `[-n, --name] <FILENAME>` - filename for archived db

### `[consume]`

#### ARGS
- `<FILEPATH>` - file path to csv file

#### KWARGS
- `[-p, --path] <FILEPATH>` - file path to csv file

### `[dump]`

#### ARGS
- `<FILEPATH>` - file path to csv file

#### KWARGS
- `[-p, --path] <FILEPATH>` - file path to csv file

### `[export]`

#### ARGS
- `<DIRPATH>` - filepath in which to save db

#### KWARGS
- `[-p, --path] <DIRPATH>` - filepath in which to save db

### `[link]`

#### ARGS
- `<FILENAME>` - filepath to database file to link

#### KWARGS
- `[-f, --file] <FILENAME>` - path to database file to link
- `[-a, --archive] <INT>` - archive number to link to db

### `[list]`

#### ARGS
- `["", all]` - list vlt config settings
- `[archives]` - list archive paths and index values
- `[name]` - list current db name
- `[cmd]` - list available vlt command aliases

### `[make]`

#### KWARGS
- `[-v, --via] <hex|uuid|random|*>` - mode for password generation
- `[-l, --length] <INT>` - password length
- `[-o, --omit] <STRING>` - string of characters to omit

### `[reset]`

#### ARGS
- `[table] -> [y/n]` - reset/clear table
- `[key] -> [y/n]` - change encryption key
- `[db] -> [y/n] ` - reset db file
- `[app] -> [y/n]` - delete all internal db/config files

### `[settings]`

#### KWARGS
- `[-fmt, --format] <v|h|df>` - default print format
- `[-l, --lenght] <INT>` - default password length
- `[-o, --omit] <STR>` - default string of characters to omit
- `[-v, --via] <uuid|hex|random|*>` - default mode for password generation

\* --via can also include any combination of the following strings: lower, upper, alpha, numeric, punctuation

### `[ipython]`

ARGS:
- `<ipython>` - opens ipython console with vlt Session() in scope as "self"

### Miscellanious

KWARGS:
- `[-cp, --clip] <s|u|p|**>` - copy search/make result to clipboard
- `[-j, --just] <s|u|p|>` - return the literal string of the requested object
- `[-t] <INT>` - length of time where copy is active
- `[-k, --key] <KEY>` - encryption key (not recommended to pass as flag, if absent vlt will prompt for it.)

\*\* any combination of chars is allowed. Add 'd' to display before copy sequence.

interactive mode
================

`vlt -i`

interactive mode takes procedural commands via either text
or number, as depicted in each provided menu. I.E. given

| 1) continue | 2) exit |

the exit can be triggered by passing either `2` or `exit`.

about
=====

This password manager is a simple SQLite database which uses symmetric encryption for persistent storage. The database currently handles source, username, and password attributes.
