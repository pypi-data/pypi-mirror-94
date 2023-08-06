# The ioProc workflow manager
ioProc is a light-weight workflow manager for Python ensuring robust, scalable and reproducible data pipelines. The tool is developed at the German Aerospace Center (DLR) for and in the scientific context of energy systems analysis, however, it is widely applicable in other scientific fields.

## how-to install
Setup a new Python environment and install ioProc using 

    pip install ioproc   

## how-to configure

Configure your pipeline in the `user.yaml`. The `workflow` is defined by a list of actions. These must
contain the fields `project`, `call` and `data` (with sub fields `read_from_dmgr`, and `write_to_dmgr`). The user
may specify additional fields for each action under the optional key `args`.  
You may get inspiration from the default actions in `general.py`.

## default actions provided by ioProc

### readExcel
This function is used to parse Excel files and storing it in the Data manager.
    
    @action('general')
    def parse_excel(dmgr, config, params):
        '''
          Parses given `excelFile` for specified `excelSheets` as dataframe object and stores it in the datamanager by the 
          key specified in `write_to_dmgr`.
          `excelHeader` can be set to `True` or `False`.
          
          The action may be specified in the user.yaml as follows:
            - action:
                project: general
                call: parse_excel
                data:
                  read_from_dmgr: null
                  write_to_dmgr: parsedData
                args:  
                  excelFile: spreadsheet.xlsx
                  excelSheet: sheet1
                  excelHeader: True
        '''
    
        args = params['args']
        file = get_field(args, 'excelFile')
        excel_sheet = get_excel_sheet(args)
        header = get_header(get_field(args, 'excelHeader'))
        parsed_excel = pd.read_excel(io=file, sheet_name=excel_sheet, header=header)
    
        with dmgr.overwrite:
            dmgr[params['data']['write_to_dmgr']] = parsed_excel

### checkpoint
Checkpoints save the current state and content of the data manger to disk in HDF5 format. The workflow can be resumed at any time from previously created checkpoints.

    @action('general')
    def checkpoint(dmgr, config, params):
        '''
        creates a checkpoint file in the current working directory with name
        Cache_TAG while TAG is supplied by the action config.
    
        :param tag: the tag for this checkpoint, this can never be "start"
        '''
        assert params['tag'] != 'start', 'checkpoints can not be named start'
        dmgr.toCache(params['tag'])
        mainlogger.info('set checkpoint "{}"'.format(params['tag']))

### printData
This action prints all data stored in the data manager to the console. It can therefore be used for conveniently debugging a workflow.

    @action('general')
    def printData(dmgr, config, params):
        '''
        simple debugging printing function. Prints all data in the data manager.
    
        Does not have any parameters.
        '''
        for k, v in dmgr.items():
            mainlogger.info(k+' = \n'+str(v))
