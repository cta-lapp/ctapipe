def build_command(executable,  input_file, output_dir=None,
                  out_extension=None, source_dir=None, options=None, append_to_file = None):
    # remove full path before file name
    output_file = input_file.split('/')[-1]
    # replace extension if need
    if append_to_file:
        output_file, extension = output_file.rsplit('.', 2)  # remove old_extension
        output_file = output_file + append_to_file + '.' + extension

    if out_extension:
        output_file = output_file.rsplit('.', 2)[0]  # remove old_extension
        output_file += "." + out_extension     # add new extension
    # build command
    if source_dir:
        input_file = source_dir + '/' + input_file
    cmd = [executable, '-i', input_file]
    if output_dir:
        cmd.append("-o")
        output_file = output_dir + "/" + output_file
        cmd.append(output_file)
    if options:
        for option in options:
            cmd.append(option)
    return cmd, output_file
