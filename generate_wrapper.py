import glob
import copy
states = ['outside','in module', 'in function']
all_sources = glob.glob('aspic-0.3.2/src/*/*90', recursive=False)
debug_function_name = 'testtest'
header_file_lines = []
pyx_file_lines = []
public_functions = set()
for source_file in all_sources:
    with open(source_file) as fin:
        state = 0
        modulename = ''
        for line in fin:
            line = line.strip()
            if not line or line[0] == '!':
                continue
            if 'public' in line:
                line = line[(line.find('public') + 7):]
                pubfuns = {s.strip() for s in line.split(',')}
                public_functions.update(pubfuns)
                continue

            current_state = states[state]
            if current_state == 'outside':
                # Look for module
                if 'module' in line.lower():
                    state = 1
                    module_name = line.split()[1]
                    continue

            elif current_state == 'in module':
                # Look for termination of module or new entries
                if 'end module' in line.lower():
                    state = 0
                    module_name = ''
                    continue
                if 'function' in line.lower() or 'subroutine' in line.lower():
                    is_function = ('function' in line.lower())
                    is_recursive = ('recursive function' in line.lower())

                    state = 2
                    type_arg_dict = {}

                    if is_function:
                        function_name_and_args = line[(line.lower().find('function') + 9):]
                    else:
                        function_name_and_args = line[(line.lower().find('subroutine') + 11):]

                    try:
                        tmp = function_name_and_args.split('(')
                        function_name, function_args = tmp[0], tmp[1]
                    except:
                        print('Here!')
                        print(line)
                        print(function_name_and_args)
                        stop
                    if function_name == debug_function_name:
                        print(line)
                        print(function_name_and_args)
                        print(function_args)
                        print(function_args.split(')')[0])
                        print(function_args.split(')')[0].split(','))
                    function_args = function_args.split(')')[0]
                    function_args = function_args.split(',')
                    function_args = [s.strip() for s in function_args if len(s.strip()) > 0]

                    type_arg_list = copy.deepcopy(function_args)
                    if is_function:
                        type_arg_list.append(function_name)
                        type_arg_dict[function_name] = 'double'
                    else:
                        type_arg_dict[function_name] = 'void'

            elif current_state == 'in function':
                # Look for missing argument definitions
                if function_name == debug_function_name:
                    print(type_arg_list, line)
                for arg in type_arg_list:
                    if arg.lower() in line.lower() and '::' in line:
                        if 'integer' in line.lower():
                            type_arg_dict[arg] = 'int'
                        elif 'real' in line.lower():
                            type_arg_dict[arg] = 'double'
                        elif 'complex' in line.lower():
                            type_arg_dict[arg] = 'complex'
                        elif 'logical' in line.lower():
                            type_arg_dict[arg] = 'bint'
                        else:
                            type_arg_dict[arg] = 'void'

                if f'end function {function_name}' in line.lower() or f'end subroutine {function_name}' in line.lower():
                    state = 1
                    if is_recursive or module_name in {'inftools', 'kksfreheat', 'kksfsrevol'}:
                        continue
                    if function_name in type_arg_dict and type_arg_dict[function_name] == 'bint':
                        continue
                    if function_name not in public_functions:
                        continue
                    has_voids = False
                    try:
                        for key in function_args:
                            if type_arg_dict[key] == 'void' or type_arg_dict[key] == 'bint' or type_arg_dict[key] == 'complex':
                                has_voids = True
                                break
                        if has_voids:
                            continue
                    except:
                        continue
                    argstring = ', '.join([type_arg_dict[key] + '* ' + key for key in function_args])
                    thestring = f'{type_arg_dict[function_name]} __{module_name}_MOD_{function_name}({argstring})'
                    header_file_lines.append(thestring)
                    #print(thestring)

                    # Build pyx wrapper
                    if is_function:
                        argstring = ', '.join([type_arg_dict[key] + ' ' + key for key in function_args])
                        pyx_list = []
                        pyx_list.append(f'cpdef {function_name}({argstring}):')
                    #for arg in function_args:
                    #    pyx_list.append(f'    cdef {type_arg_dict[arg]} {arg}')
                        argstring = ', '.join(['&' + key for key in function_args])
                        call_string = f'__{module_name}_MOD_{function_name}({argstring})'
                        pyx_list.append(f'    cdef {type_arg_dict[function_name]} res = {call_string}')
                        pyx_list.append(f'    return res')
                        pyx_file_lines += pyx_list


type_subs = {'complex':'double complex', 'bint':'bool'}
for index, line in enumerate(header_file_lines):
    if 'lambda' in line:
        header_file_lines[index] = line.replace('lambda','_lambda')
    for cythontype, ctype in type_subs.items():
        header_file_lines[index] = header_file_lines[index].replace(cythontype, ctype)

for index, line in enumerate(pyx_file_lines):
    if 'lambda' in line:
        pyx_file_lines[index] = line.replace('lambda','_lambda')

with open('aspic.h', 'w') as h_file:
    with open('cpyaspic.pxd', 'w') as pxd_file:
        pxd_file.write('cdef extern from "aspic.h":\n')
        for line in header_file_lines:
            h_file.write(line + ';\n')
            pxd_file.write('    ' + line.replace('bool','bint') + '\n')
with open('pyaspic.pyx', 'w') as pyx_file:
    pyx_file.write('#include <stdbool.h>\n')
    pyx_file.write('#include <complex.h>\n')
    pyx_file.write('from cpyaspic cimport *\n')
    for line in pyx_file_lines:
        pyx_file.write(line + '\n')
