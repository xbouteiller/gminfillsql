from sqlite3 import Error
import sqlite3
import shutil


##########################################################################################################################################
#config


dbName = 'DataBase.db'

tablename = 'gminallometry'

##########################################################################################################################################
input_prompts = {
    
    'sp':'Species (default p.p.): ',
    's':'Site: ',
    't':'Treatment: ',    
    'tr':'Tree Number: ',
    'rep': 'Repetition: ',
    'length':'needle or leaf length (cm): ',
    'width':'needle or leaf width (mm): ', 
    'thickness':'needle or leaf thickness (mm): ',    
    'fw':'Fresh Weight (g): ',
    'ow':'Output Weight (g): ',
    'dw':'Dry Weight (g): ',
    'note': 'Note: '
}


sql_create_wp_table = """ CREATE TABLE IF NOT EXISTS {}(
        number INTEGER PRIMARY KEY,
        campaign varchar(50),
        species varchar(30) NOT NULL,
        site varchar(30) NOT NULL,
        treatment varchar(30) NOT NULL,
        tree INTEGER NOT NULL,
        rep INTEGER,
        length real,
        width real,
        thickness real,           
        freshweight real,
        outputweight real,
        dryweight real,
        code varchar(100) UNIQUE,
        note varchar(100)
        ); """.format(tablename)

sql_create_site_table = """ CREATE TABLE IF NOT EXISTS siteinfo(
        number INTEGER PRIMARY KEY,
        campaign varchar(50),
        site varchar(30),
        date varchar(10),
        X real,
        Y real,               
        temperature real,
        hygro real,
        FOREIGN KEY (site) REFERENCES {}(site)
        ); """.format(tablename)
        
dbcolname = {    
    'sp':'species',
    's':'site',
    't':'treatment',    
    'tr':'tree',
    'rep':'repetition',
    'length':'length',
    'width':'width',
    'thickness':'thickness',
    'fw':'freshweight',
    'ow':'outputweight',
    'dw':'dryweight',
    'note':'note'
}


insert_sql = """
        INSERT INTO {}(campaign, species, site, treatment, tree, rep, length, width, thickness, freshweight, outputweight, dryweight, code, note)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """.format(tablename)

insert_sql_site = """
        INSERT INTO siteinfo(campaign, site, date, X, Y, temperature, hygro)
        VALUES (?,?,?,?,?,?,?)
        """
##########################################################################################################################################

class SamplingDataBase():
    from sqlite3 import Error
    import sqlite3
    def __init__(self, dbn, ip, scwp, ist, dbcn, ists, scst):

        self.dbName = dbn
        self.input_prompts = ip
        self.sql_create_wp_table = scwp
        self.insert_sql = ist
        self.dbcolname = dbcn
        self.insert_sql_site = ists
        self.sql_create_site_table = scst

        # options allowed for the action method
        self.choices = {
        "1": self._instantiate,
        "2": self._modify,
        "3": self._site,
        "4": self._append,
        "5": self._quit,
        # "4": self.erase,
        # "5": self.extract_strings_and_nums
        }

    def display_menu(self):
        print("""
        --------------------
        -----   MENU   -----
        --------------------

        List of actions

        1. Instantiate or complete a data base
        2. Modify values
        3. Fill site table
        4. Enter values for a column
        5. Exit


        """)


    def run(self):
        '''Display the menu and respond to choices.'''

        while True:
            self.display_menu()
            choice = input("Enter an option: ")

            # redirection to the self.choices attribute in the __init__
            action = self.choices.get(choice)

            if action:
                action()
            else:
                print("{0} is not a valid choice".format(choice))
                self.run()
            
            self.action_choice = choice


    def _quit(self):
        import sys
        print("Thank you for using your sampling data base today.\n")
        # self.view_db()
        sdb._view_summary()
        sys.exit(0)


    def _get_valid_input(self, input_string, valid_options):
        '''
        useful function in order to ask input value and assess that the answer is allowed

        input_string : question
        valid_options : authorized answers
        '''
        input_string += "({}) ".format(", ".join(valid_options))
        response = input(input_string)
        while response.lower() not in valid_options:
            response = input(input_string)
        return response

    def _create_connection(self, db_file):
        """ create a database connection to the SQLite database
            specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
        import sqlite3
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Error as e:
            print(e)

        return conn

    def _create_table(self, conn, create_table_sql):
        """ create a table from the create_table_sql statement
        :param conn: Connection object
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """
        try:
            c = conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(e)

    def view_db(self):
        conn = self._create_connection(self.dbName)    
        for row in conn.execute('SELECT * FROM {}'.format(tablename)):
            print(row)

    def view_db_s(self):
        conn = self._create_connection(self.dbName)     
        for row in conn.execute('SELECT * FROM siteinfo'):
            print(row)

    def _create_wp(self, conn, sqltable, wpvalue):
        """
        Create a new project into the projects table
        :param conn:
        :param project:
        :return: project id
        """
        sql = sqltable
        cur = conn.cursor()
        cur.execute(sql,wpvalue)
        conn.commit()
        # conn.commit()
        print('>>> Specimen data entered successfully\n')

    def _instantiate(self):

        conn = self._create_connection(self.dbName)
        # create tables
        if conn is not None:
            # create projects table
            self._create_table(conn, self.sql_create_wp_table)
            # # create tasks table
            # self._create_table(conn, sql_create_tasks_table)
        else:
            print("Error! cannot create the database connection.")

        responses = []
        self.site = None
        self.treen = 1
        self.rep = 1
        self.treat = None

        campaign_name = input('\nwhat is the campaign name? ')

        while True:
            behav = input('\nBehaviour: do you have samples\' repetition (\'y\' default, \'n\')? ') or 'y'
            if behav not in ['y', 'n']:
                print('oops: should be y or n')
            else:
                break
        if behav == 'y':
            nofrepet = input('How many repetition do you have (default 2)? ' ) or '2'
            while True:                    
                try:
                    nofrepet = int(nofrepet)
                    break
                except:
                    print('Can\'t be converted to integer, try again ...')

        incr = 0
        prev_site = None
        prev_treat = None
        
        while True:           

            print('\nEnter your values\n--------------------------------')

            
            
            for key in self.input_prompts: # loop over our prompts
            

                if key == 'sp':
                    response = input(input_prompts[key] + ' (default p. pinaster) ') or 'pinus pinaster'

                elif (key=='s'):
                        if (self.site is None):
                            response = input('Site: ')
                            self.site = response
                        else:
                            response = input('Site: (default: {}) '.format(self.site)) or self.site
                            #response = self.site
                            self.site = response

                elif key == 't':
                    if self.treat is None:
                        response = input(input_prompts[key])
                        self.treat = response
                    else:
                        response = input(input_prompts[key] + ' (default: {}) '.format(self.treat)) or self.treat                       
                        self.treat = response
                        
                                     
                    response = response

                elif key == 'tr':
                    # print(self.site)
                    # print(prev_site)
                    # print(incr != 0 and (self.site != prev_site or self.treat != prev_treat))
                    if incr != 0 and (self.site != prev_site or self.treat != prev_treat):
                        self.rep = 1
                        self.treen = 1
                    response = input(self.input_prompts[key]+ ' (or {}) '.format(self.treen)) or self.treen
                    self.treen = int(response)

                    if behav == 'n':
                        self.treen += 1                  
                                            

                elif key == 'rep':
                    response = input(self.input_prompts[key]+ ' (or {}) '.format(self.rep)) or self.rep
                    self.rep = int(response)

                    if behav == 'y':
                        self.rep += 1
                        if self.rep == nofrepet+1:
                            self.rep = 1
                        if self.rep == 1 and incr !=0:
                            self.treen += 1

                    prev_site = self.site
                    prev_treat = self.treat  
                    incr += 1
                    #print('incr: ', incr)
           


                else:
                    response = input(self.input_prompts[key])

                if (key=='tr'):
                    try:
                        response = int(response)
                    except:
                        print('Can\'t be converted to an integer, Set to None')
                        response = None

                if (key=='length') | (key=='width') | (key=='thickness') | (key=='fw') | (key=='ow') | (key=='dw'):
                    try:
                        response = float(response)
                    except:
                        #print(key)
                        response = None

                    if response is None and (self.rep-1 == 1 and incr == 1):
                        print('turned to -99')
                        response = -99
                    elif response is None and (self.rep-nofrepet+1 == 1 and incr != 1):
                        print('turned to -99')
                        response = -99
                    else:
                        pass
                    #     print('pass')
                    # print(self.rep-nofrepet+1)

                if key == 'rep':
                    try:
                        response = int(response)
                    except:
                        response = None
               
                if (key == 'note' ) & (response == ''):
                    response = ''
                                
                if response == 'exit':
                    break # break out of for loop

                responses.append(response)

            if response == 'exit':                
                break

            print('\nresp :', responses, '\n')
            # c_number, c_species, c_site, c_treatment, c_psipredawn, c_psimidday, c_freshweight, c_rehydratedweight, c_dryweight = responses
            c_species, c_site, c_treatment, c_tree, c_rep, c_length, c_width, c_thin, c_freshweight, c_outputweight, c_dryweight, c_note = responses
            c_code = '_'.join([campaign_name, c_species, c_site, c_treatment,str(c_tree), str(c_rep)])

            # self._create_wp(conn, self.insert_sql, (c_number, c_species, c_site, c_treatment, c_psipredawn, c_psimidday, c_freshweight, c_rehydratedweight, c_dryweight) )
            self._create_wp(conn, self.insert_sql, (campaign_name, c_species, c_site, c_treatment, c_tree, c_rep, c_length, c_width, c_thin, c_freshweight, c_outputweight, c_dryweight, c_code, c_note) )

            responses.clear() # clear our responses, before we start our new while loop iteration
            self.view_db()


        conn.close()

    def _update_task(self, conn, tasks, param):
        sql = '''
                UPDATE {}
                SET {} = ? 
                WHERE code = ?       
        '''.format(tablename, param)
        cur = conn.cursor()
        cur.execute(sql, tasks)
        conn.commit()
        print('>>> Specimen {} modified successfully\n'.format(param))

        
    def _modify(self):

        conn = self._create_connection(self.dbName)
        # create tables
        if conn is not None:
            # create projects table
            self._create_table(conn, self.sql_create_wp_table)
            # # create tasks table
            # self._create_table(conn, sql_create_tasks_table)
        else:
            print("Error! cannot create the database connection.")

        while True:
            vartoupdate = input('\nWhich variable do you want to update ? ')
            if vartoupdate not in list(input_prompts.keys()):
                print('oops, should be one of: ', list(input_prompts.keys()))                
            else:
                break

        campaign_name = input('\nwhat is the campaign name? ')

        print(vartoupdate)
        vtu = vartoupdate
        vartoupdate = self.dbcolname[vartoupdate]
        print(vartoupdate)
            # vartoupdate = self._get_valid_input('Which variable do you want to update ?',input_prompts.keys)
        responses = []
        self.site = None
        self.treen = 1
        self.rep = 1
        self.treat = None

        while True:
            behav = input('\nBehaviour: do you have samples\' repetition (\'y\' default, \'n\')? ') or 'y'
            if behav not in ['y', 'n']:
                print('oops: should be y or n')
            else:
                break
        if behav == 'y':
            nofrepet = input('How many repetition do you have (default 2)? ' ) or '2'
            while True:                    
                try:
                    nofrepet = int(nofrepet)
                    break
                except:
                    print('Can\'t be converted to integer, try again ...')
        incr = 0
        prev_site = None
        prev_treat = None

        while True:

            print('\nEnter your values\n--------------------------------')

            for key in ['sp', 's', 't', 'tr', 'rep', vtu]:       

                if key == 'sp':
                    response = input(input_prompts[key] + ' (default p. pinaster) ') or 'pinus pinaster'
                    
                elif (key=='s'):
                        if (self.site is None):
                            response = input('Site: ')
                            self.site = response
                        else:
                            response = input('Site: (default {}) '.format(self.site)) or self.site
                            self.site = response

                elif key == 't':
                    if self.treat is None:
                        response = input(input_prompts[key])
                        self.treat = response

                    else:
                        response = input(input_prompts[key] + ' (default: {}) '.format(self.treat)) or self.treat            
                        self.treat = response                   

                elif key == 'tr':
                    # print(self.site)
                    # print(prev_site)
                    # print(incr != 0 and (self.site != prev_site or self.treat != prev_treat))
                    if incr != 0 and (self.site != prev_site or self.treat != prev_treat):
                        self.rep = 1
                        self.treen = 1
                    response = input(self.input_prompts[key]+ ' (or {})  '.format(self.treen)) or self.treen
                    self.treen = int(response)
                    if behav == 'n':
                        self.treen += 1
                    

                elif key == 'rep':
                    response = input(self.input_prompts[key]+ ' (or {}) '.format(self.rep)) or self.rep
                    self.rep = int(response)                    

                    if behav == 'y':
                        self.rep += 1
                        if self.rep == nofrepet+1:
                            self.rep = 1
                        if self.rep == 1 and incr !=0:
                            self.treen += 1 

                    prev_site = self.site
                    prev_treat = self.treat              
                    incr += 1 
                    
                else:
                    response = input(self.input_prompts[key])

                if (key=='length') | (key=='width') | (key=='thickness') | (key=='fw') | (key=='rw') | (key=='dw'):
                    try:
                        response = float(response)
                    except:
                        print('Failed to convert to float, turned to None')
                        response = None
                    
                    if response is None and (self.rep-1 == 1 and incr == 1):
                        print('turned to -99')
                        response = -99
                    elif response is None and (self.rep-nofrepet+1 == 1 and incr != 1):
                        print('turned to -99')
                        response = -99
                    else:
                        pass


                if response == 'exit':
                    break # break out of for loop

                responses.append(response)

            if response == 'exit':                
                break

            print('\nresp :', responses, '\n')
            c_species, c_site, c_treatment, c_tree, c_rep, c_var = responses
            c_code = '_'.join([campaign_name, c_species, c_site, c_treatment, str(c_tree), str(c_rep)])

            self._update_task(conn, (c_var, c_code), vartoupdate)
       
            responses.clear()
            self.view_db()


        conn.close()

    def _update_task_fk(self, conn, tasks, param):
        sql = '''
                UPDATE {}
                SET {} = ? 
                WHERE number = ?       
        '''.format(tablename, param)
        cur = conn.cursor()
        cur.execute(sql, tasks)
        conn.commit()
        print('>>> Specimen {} modified successfully as {}\n'.format(param, tasks[0]))
            


    def _append(self):

        conn = self._create_connection(self.dbName)
        # create tables
        if conn is not None:
            self._create_table(conn, self.sql_create_wp_table) 
        else:
            print("Error! cannot create the database connection.")

        while True:
            vartoupdate = input('Which column do you want to fill ? ')
            colttofill = list(self.dbcolname.keys())[5:]
            if vartoupdate not in colttofill:
                print('oops, should be one of: ', colttofill)                
            else:
                break

        print(vartoupdate)
        vtu = vartoupdate
        vartoupdate = self.dbcolname[vartoupdate]
        print(vartoupdate)
          
        response = input('Site: ') or None
        self.site = response

        iterator = conn.cursor()

        if self.site is not None:
            iterator.execute("SELECT * FROM {} WHERE site LIKE '{}'".format(tablename, self.site))
        else:                       
            response = input('From number: ') or None
            if response is not None:
                iterator.execute('SELECT * FROM {} WHERE number > {}'.format(tablename, str(int(response)-1)))
            else:
                iterator.execute('SELECT * FROM {}'.format(tablename))

        print('\n')

        existingcol = [vartoupdate == description[0] for description in iterator.description]
        #print('existingcol: ', existingcol)
        existingcol = [i for i, x in enumerate(existingcol) if x][0]
        for row in iterator:
            uniquekey = row[0]
            print('species : {0}, site: {1}, treatment: {2}, tree: {3}, rep: {4}'.format(row[2], row[3], row[4],row[5], row[6]))
            existingval = row[existingcol]

            valtofill = input('{} value (existing: {}): '.format(vartoupdate, existingval)) or existingval

            if valtofill == 'exit' or valtofill == 'e':
                break
            else:
                while True: 
                    if valtofill is not None:
                        try:
                            valtofill = float(valtofill)
                            break
                        except:
                            print('oops, value can\'t be converted to float')
                            valtofill = input('{} value: '.format(vartoupdate))

                    else:
                        break
                
                if valtofill == -99:
                    valtofill = -99                        
                       
                self._update_task_fk(conn, (valtofill, uniquekey), vartoupdate)
        conn.close()

    def _site(self):

        conn = self._create_connection(self.dbName)
        # create tables
        if conn is not None:
            # create projects table
            self._create_table(conn, self.sql_create_site_table)

        else:
            print("Error! cannot create the database connection.")

        responses = []
        self.site = None

        campaign_name = input('\nwhat is the campaign name? ')

        while True:           

            print('\nEnter your values\n--------------------------------')
            
            
            for key in ['Site: ', 'Date (yyyy/mm/dd):' , 'X: ', 'Y: ', 'Temp: ', 'Hygro: ' ]: # loop over our prompts
                response = input(key)
                if (key=='X: ') | (key=='Y: ') | (key== 'Temp: ') | (key=='Hygro: '):

                    
                    try:
                        response = float(response)
                    except:
                        response = None

                if response == 'exit':
                    break # break out of for loop

                responses.append(response)

            if response == 'exit':                
                break

            print('\nresp :', responses, '\n')
            c_site, c_date, c_x, c_y, c_temp, c_hygro = responses

            self._create_wp(conn, self.insert_sql_site , ( campaign_name, c_site, c_date, c_x, c_y, c_temp, c_hygro) )

            responses.clear() # clear our responses, before we start our new while loop iteration
            self.view_db_s()


        conn.close()
    
    def _view_summary(self):
        import pandas as pd
        conn = self._create_connection(self.dbName)

        df = pd.read_sql_query('SELECT * FROM {}'.format(tablename), conn)
        while True:
            behav = input('Do you want to fill Na by previous value? (y, n) ') or 'y'
            if behav not in ['y', 'n']:
                print('oops: should be y or n')
            else:
                break
        if behav:
            print('Na filled forward')
            df = df.fillna(method='ffill' )        

        df.to_csv(tablename+'.csv')

        print(df.groupby(['campaign','site', 'treatment']).mean())




if __name__ == '__main__':
    try:
        shutil.copy2(dbName, dbName + '_bak')
        print('\nBack up created')
    except:
        print('\nno DB file detected')    
    sdb = SamplingDataBase(dbName, input_prompts, sql_create_wp_table, insert_sql, dbcolname, insert_sql_site, sql_create_site_table)
    sdb.run()
    
    # sdb.view_db()
