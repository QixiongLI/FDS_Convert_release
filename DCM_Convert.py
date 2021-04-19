import clr
import os
import numpy as np
from Periphery import Counter
#pyinstaller --onefile -w FDS_Convert.py

def edxx2dcm(tk_psw, file_name_edxx):

    def create_dcm_directory(path_dcm):
        if not (os.path.exists(path_dcm) and os.path.isdir(path_dcm)):
            try:
                os.mkdir(path_dcm)
            except OSError:
                result_dir = f'Creation of the directory failed with \n   {path_dcm}'
            else:
                result_dir = f'Successfully created the directory with \n   {path_dcm}'
        else:
            result_dir = f'Directory is already exited with \n   {path_dcm}'
        return result_dir

    def write_dcm_head(fid):
        fid.write('\n')
        fid.write('KONSERVIERUNG_FORMAT 2.0')
        fid.write('\n\n')
        fid.close()

    def write_dcm_value(fid, value_z, value_z_unit, dcm_label_name, parameter_longname):
        fid.write(f'FESTWERT {dcm_label_name}\n')
        fid.write(f'   LANGNAME \"{parameter_longname}\"\n')
        if value_z_unit == "None":
            fid.write(f'   EINHEIT_W \"\"\n')
        else:
            fid.write(f'   EINHEIT_W \"{value_z_unit}\"\n')
        fid.write(f'   WERT %.3f\n' % value_z)
        fid.write('END\n\n')
        fid.close()

    def write_dcm_curve(fid, value_x, value_x_unit, value_z, value_z_unit, dcm_label_name, parameter_longname):
        fid.write(f'KENNLINIE {dcm_label_name} {len(value_x)}\n')
        fid.write(f'   LANGNAME \"{parameter_longname}\"\n')
        if value_x_unit == "None":
            fid.write(f'   EINHEIT_X \"\"\n')
        else:
            fid.write(f'   EINHEIT_W \"{value_x_unit}\"\n')
        if value_z_unit == "None":
            fid.write(f'   EINHEIT_W \"\"\n')
        else:
            fid.write(f'   EINHEIT_W \"{value_z_unit}\"\n')
        fid.write(f'   ST/X')
        for num_value_x in value_x:
            fid.write(f'   %.3f' % num_value_x)
        fid.write(f'\n')
        fid.write(f'   WERT')
        for num_value_z in value_z:
            fid.write(f'   %.3f' % num_value_z)
        fid.write(f'\n')
        fid.write('END\n\n')
        fid.close()

    def write_dcm_map(fid, value_x, value_x_unit, value_y, value_y_unit, value_z, value_z_unit, dcm_label_name,
                      parameter_longname):
        fid.write(f'KENNFELD {dcm_label_name} {len(value_x)} {len(value_y)}\n')
        fid.write(f'   LANGNAME \"{parameter_longname}\"\n')
        if (value_x_unit == "None"):
            fid.write(f'   EINHEIT_X \"\"\n')
        else:
            fid.write(f'   EINHEIT_X \"{value_x_unit}\"\n')
        if (value_y_unit == "None"):
            fid.write(f'   EINHEIT_Y \"\"\n')
        else:
            fid.write(f'   EINHEIT_Y \"{value_y_unit}\"\n')
        if (value_z_unit == "None"):
            fid.write(f'   EINHEIT_W \"\"\n')
        else:
            fid.write(f'   EINHEIT_W \"{value_z_unit}\"\n')
        fid.write(f'   ST/X')
        for num_value_x in value_x:
            fid.write(f'   %.3f' % num_value_x)
        fid.write(f'\n')
        ind = int(value_z.shape[0])
        for num_value_y in reversed(value_y):
            fid.write(f'   ST/Y')
            fid.write(f'   %.3f' % num_value_y)
            fid.write(f'\n')
            fid.write(f'   WERT')
            for j in range(value_z.shape[1]):
                fid.write(f'   %.3f' % value_z[ind - 1, j])
            ind -= 1
            fid.write(f'\n')
        fid.write('END\n\n')
        fid.close()


    parameter_counter = Counter(0, 0, 0, 0)
    cwd_path = os.getcwd()
    full_interface_path = cwd_path + '\\MDT.ParameterInterface_1.1.0\\MDT.ParameterInterface.dll'
#sys.path.append("D:\\CatIsAnimal\\Convert\\MDT.ParameterInterface_1.1.0\\")
#clr.AddReference("D:\\CatIsAnimal\\Convert\\MDT.ParameterInterface_1.1.0\\MDT.ParameterInterface.dll")

    clr.AddReference(full_interface_path)
    from MDT.ParameterInterface import ExpertDataService, ExpertDataTypes
    # token_password = "Sommer2016"
    # file_name = "D://CatIsAnimal//Convert//temp//FDS_MainInjBegin_L_48-60_CR_B2_514_Marine_DE_1080kW.edxx"
    token_password = tk_psw
    file_name = file_name_edxx

    # create path and write dcm file
    path_dcm = os.path.split(file_name)[0] + "/DCM"
    result_dir = create_dcm_directory(path_dcm)
    file_name_dcm = path_dcm + "\\" + os.path.split(file_name)[1].replace("edxx", "dcm")
    fid = open(file_name_dcm, "w")
    write_dcm_head(fid)


    serviceinstance = ExpertDataService()
    serviceinstance.Initialize(token_password)
    try:
        file_read = serviceinstance.CreateReader(file_name)
    except Exception as exception:
        # return exception
        raise
    # file_read = serviceinstance.CreateReader(file_name)
    ParameterCount = file_read.GetParameterCount()
    types = ExpertDataTypes()

    parameter = []
    dcm_label_name = ""
    parameter_longname = ""
    for index_i in range(ParameterCount):
        parameter.append(file_read.GetParameter(index_i))
        if not (parameter[index_i].IsOpv):
            # test = not (parameter[index_i].IsOpv)
            temp_name = parameter[index_i].Name
            # Temp_Name = "_jdsfakljfsa:dk_doemlk.,faa"
            for ch in ['\\', '`', '*', ',', '{', '}', '[', ']', '(', ')', '>', '#', '+', '-', '.', '!', '$', '\'',
                       ':', '°', '|', '=', '/', ' ']:
                temp_name = temp_name.replace(ch, '_')
            temp_name = temp_name.replace('__', '_')
            temp_id = parameter[index_i].Id
            temp_id_split = temp_id.split('-')
            temp_id_split[0] = str(format(int(temp_id_split[0]), '03d'))
            s_id = "_"
            temp_id_out = s_id.join(temp_id_split)
            dcm_label_name = ("ID_" + temp_id_out + "_" + temp_name)
            parameter_longname = ("ExpertDataType: " + parameter[index_i].ExpertDataType + "/+/" +
                                    'ReadLevel: ' + str(parameter[index_i].ReadLevel) + '/+/' +
                                    'WriteLevel: ' + str(parameter[index_i].WriteLevel) + '/+/' 
                                    'IsImoRelevant: ' + str(int(parameter[index_i].IsImoRelevant)) + '/+/'
                                    'IsConfigureMode: ' + str(int(parameter[index_i].IsConfigureMode)) + '/+/'
                                    'IsOpv: ' + str(int(parameter[index_i].IsOpv)) + '/+/' +
                                    'IsStructural: ' + str(int(parameter[index_i].IsStructural)) + '/+/' +
                                    'SizeX: ' + str(parameter[index_i].SizeX) + '/+/' +
                                    'SizeY: ' + str(parameter[index_i].SizeY) + '/+/' +
                                    'LowerLimit: ' + str(parameter[index_i].GetLowerLimit()) + '/+/' +
                                    'UpperLimit: ' + str(parameter[index_i].GetUpperLimit()) + '/+/' +
                                    'ParentID: ' + str(parameter[index_i].ParentId) + '/+/'
                                    'Name: ' + str(parameter[index_i].Name) + '/+/' +
                                    'Unit: ' + str(parameter[index_i].Unit) + '/+/' +
                                    'UnitX: ' + str(parameter[index_i].UnitX) + '/+/' +
                                    'UnitY: ' + str(parameter[index_i].UnitY)
                                    )
            value_x = []
            value_z = []
            value_y = []
            value_x_unit = ""
            value_z_unit = ""
            value_y_unit = ""
            if parameter[index_i].ExpertDataType =='REAL':
                value_z = float(parameter[index_i].GetValue())
                value_z_unit = str(parameter[index_i].Unit)
                fid = open(file_name_dcm, "a")
                write_dcm_value(fid, value_z, value_z_unit, dcm_label_name, parameter_longname)
                parameter_counter.single_add()
            elif parameter[index_i].ExpertDataType == 'BOOLEAN':
                value_z = int(parameter[index_i].GetValue())
                # value_z_unit = str(parameter[index_i].Unit)
                fid = open(file_name_dcm, "a")
                write_dcm_value(fid, value_z, value_z_unit, dcm_label_name, parameter_longname)
                parameter_counter.boolean_add()
            elif parameter[index_i].ExpertDataType == 'INTEGER':
                value_z = float(parameter[index_i].GetValue())
                value_z_unit = str(parameter[index_i].Unit)
                fid = open(file_name_dcm, "a")
                write_dcm_value(fid, value_z, value_z_unit, dcm_label_name, parameter_longname)
                parameter_counter.single_add()
            elif parameter[index_i].ExpertDataType == 'CURVE':
                value_x = np.fromiter(parameter[index_i].GetXAxisValues(), float)
                value_z = np.fromiter(parameter[index_i].GetValue(), float)
                value_x_unit = str(parameter[index_i].UnitX)
                value_z_unit = str(parameter[index_i].Unit)
                fid = open(file_name_dcm, "a")
                write_dcm_curve(fid, value_x, value_x_unit, value_z, value_z_unit, dcm_label_name, parameter_longname)
                parameter_counter.curve_add()
            elif parameter[index_i].ExpertDataType == 'MAP':
                value_x = np.fromiter(parameter[index_i].GetXAxisValues(), float)
                value_y = np.fromiter(parameter[index_i].GetYAxisValues(), float)
                value_z_tmp = np.array(np.fromiter(parameter[index_i].GetValue(), float))
                value_z_tmp1 = value_z_tmp.reshape(len(value_x), len(value_y))
                value_z = value_z_tmp1.transpose()
                value_x_unit = str(parameter[index_i].UnitX)
                value_z_unit = str(parameter[index_i].Unit)
                value_y_unit = str(parameter[index_i].UnitY)
                fid = open(file_name_dcm, "a")
                write_dcm_map(fid, value_x, value_x_unit, value_y, value_y_unit, value_z, value_z_unit, dcm_label_name,
                              parameter_longname)
                parameter_counter.map_add()
    return parameter_counter, result_dir, os.path.split(file_name)[1].replace("edxx", "dcm")




#clr.AddReference("D:/CatIsAnimal/Convert/MDT.ParameterInterface_1.1.0/MDT.ParameterInterface.dll")+

