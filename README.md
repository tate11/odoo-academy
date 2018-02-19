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

### Academy Base

- [ ] Finish to integrate appointment manager with training action
    - Add a form widget
- [ ] Modify session Kanban grouping items by week day
    - Remove obsolete related server action
- [ ] Finish session creation and autocreation
    - Finally button should be create next session FROM RANGE ignoring all other things
    - Finally automated task should be create all sessions IN RANGE ignoring all other things
- [ ] Add session Kanban grouping to show items by: archived (folded), pending, working, ready
- [ ] Resource model or view fails, see log
- [x] Add a basic security descriptors
- [ ] Sort the module menus

- [ ] SESSIONS By student
- [ ] Training action progress bar should indicate units, not hours
- [ ] Fields duration and hours fails with different days in datetime bounds

- [ ] Progress bar in attendance
- [ ] Other color (or style) for finished sessions in training action view
- [ ] The model academy.training.action.unit.control has no access rules

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

### Other modules

- [ ] The model academy.rebasing.exercise.item
- [ ] The model res.partner has no access rules
- [ ] The model academy.rebasing.exercise has no access rules
- [ ] odoo.modules.graph: module auto_backup: not installable, skipped
- [ ] odoo.models: ir.actions.report.xml.write() with unknown fields: paperformat_id

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
