## Synopsis

Modules used to manage the teaching activity.


## Motivation

I don't know any open source software, and free of charge, to manage learning activities, handle contents, etc...

Now I have need to take a more comprehensive control over training activities in which I participate as teacher and I'm forced to use inadequate handling tools.

In a future I want an integral app to manage, on cloud, all the educational projects and the related activities. This software must be easy to use and agile. I'm trying to develop something like it over the Odoo ERP.


## Installation

Project can be cloned on your server using git command line, following line is an example:

```
git clone https://github.com/sotogarcia/odoo-academy.git
```

Once you have downloaded the project, you will can find the modules inside project folder, to install them in Odoo you must copy foldersinto the addons directory, alongside the official modules.

Once done, you need to update the module list before these new modules are available to install.

For this you need the Technical menu enabled, since the Update Modules List menu option is provided by it. It can be found in the Modules section of the Settings menu.

After running the modules list update you can confirm the new modules are available to install. In the Local Modules list, remove the Apps filter and search for department. You should see the new modules available.


## Modules

```
└──academy_base                   : base module required to install all others. It adds the Academy main menu.
    ├───academy_exercise_toos     : some tools to generate content
    ├───academy_online_assets     : shares a folder with some resources required for external tools
    ├───academy_public_tendering  : stores information about public tendering processes.
    ├───academy_tests             : stores questions and answeres and allows to build manual and random tests.
    └───academy_tests_web         : publish tests on Odoo website

    └───ap3_settings              : Customization for Academia Postal 3
```

####  appointment.manager

```
├───start_datetime··········: Datetime
├───allday··················: Boolean
│   └───duration············: Float
├───recurrency··············: Boolean
├───interval················: Integer
├───rrule_type··············: Selection
│   ├───daily
│   ├───weekly
│   │   ├───mo··············: Boolean
│   │   ├───tu··············: Boolean
│   │   ├───we··············: Boolean
│   │   ├───th··············: Boolean
│   │   ├───fr··············: Boolean
│   │   ├───sa··············: Boolean
│   │   └───su··············: Boolean
│   ├───monthly·············: Selection
│   │   ├───date
│   │   │   └───day·········: Integer
│   │   └───day
│   │       ├───byday·······: Selection
│   │       │   ├───First
│   │       │   ├───Second
│   │       │   ├───Third
│   │       │   ├───Fourth
│   │       │   ├───Fifth
│   │       │   └───Last
│   │       └───weeklist····: Selection
│   │           ├───MO
│   │           ├───TU
│   │           ├───WE
│   │           ├───TH
│   │           ├───FR
│   │           ├───SA
│   │           └───SU
│   └───yearly
└───end_type················: Selection
    ├───count
    │   └───count···········: Integer
    └───stop_date
        └───final_date······: Date
```

### Todo

- [ ] Update languages
- [ ] Change color to read only tabs

### Academy Base

- [ ] Finish enrolment
      - Date
      - Sequence
      - Kanban view
      - Filters

- [ ] Finish modules
      - Module must have own hours if it has not training units
      - List of available resources
      - List of students who have coursed this module
      - Modules have their own hours value if they have not units, otherwise
      the hours will be the sum of unit hours
      - **Idea**: undefined time length allowed

- [ ] Finish resource
      - Add button to set directory
      - Download as zip: directory + attachments
      - Resource shoud be linked to modules as avaliable resources (mandatory)
        - Resource shoud be linked to units (inside module)(optional)

- [ ] Finish menú
      - Change and translate Helper (menú)
      - Global menú should be sorted

- [ ] Add tutor group
      - Training actions have tutors
      - Add security desctiptor to tutors

- [ ] Add sessions
      - Sessions should be linked to actions and **modules**
        - *Optionally, sessiones can be lenked to units*
      - One session can be more than one modules/units
      - **Can be sessions without modules?**
      - **Idea**: Store first date for modules

- [ ] Ensure all models can be duplicated

- [ ] Add rules
      - Consultants (view only asigned)
      - Teachers (view only asigned units, manage own resources)
      - Tutors (view only asigned actions, their modules and units, asign teachers)


- [x] Adds training activity
- [x] Arrange training action
- [x] Revisar todas las vistas de lista
- [x] Arrange unit_count computed field in serveral models
- [x] WARNING method academy.training.action._check_end: @constrains parameter 'end' is not a field name
- [x] WARNING Field definition for _inherits reference "training_activity_id" in "academy.training.action" must be marked as "required" with ondelete="cascade" or "restrict", forcing it to required + cascade.
- [x] WARNING odoo_50110_dev_academy odoo.modules.loading: The model academy.training.action.enrolment has no access rules, consider adding one. E.g. access_academy_training_action_enrolment,access_academy_training_action_enrolment,model_academy_training_action_enrolment,base.group_user,1,0,0,0
- [x] Finish demo data
- [x] The model res.partner has no access rules
- [x] Finish security descriptors
- [x] Students should be sign up in modules but not in actions


> *Idea*:  weekly or monthy reports
> *Idea*:  unit, module, action and activity reports


#### Academy test

- [x] Test form must allow to add questions
- [ ] Lint all files
- [ ] Answer view (from menu) could not allow to create new
- [ ] Category view (from menu) could not allow to create new
- [x] Test reports should be accessible from action menu
- [ ] Link tests and resources

#### Create ap3_academy_tests

- [ ] Report format

#### Create academy_test_claim
- [ ] Impugnment must be a new module named academy_test_claim
- [ ] Claim menú should be child from menu_academy_monitoring

## Scripts

- **oaclient.py**   : client to connect to Odoo server and manage academy resources using RPC.
- **test2sql.py**   : script to transform test given as text format to an SQL script
- **gettest.py**    : client to download tests questions and answers
- **backup.py**     : client to performs a backup of the Odoo database


## Licences

* code-is-beautiful is licensed under the GNU AFFERO GENERAL PUBLIC LICENSE (Version 3). To view a copy of this license, visit [http://www.gnu.org/licenses/agpl-3.0.html](http://www.gnu.org/licenses/agpl-3.0.html).

* [![Creative Commons License](https://i.creativecommons.org/l/by-nc-sa/4.0/80x15.png)](http://creativecommons.org/licenses/by-nc/4.0/) code-is-beautiful Documentation is licensed under a [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-nc-sa/4.0/).


## Feedback

The best way to send feedback is to file an issue at [https://github.com/sotogarcia/Academia/issues](https://github.com/sotogarcia/ /issues) or to reach out to us via [twitter](https://twitter.com/jorgedenarahio) or [email](sotogarcia@gmail.com).
