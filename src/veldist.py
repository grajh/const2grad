#-*- coding: utf-8 -*-


def read_mod(mod_file, step=False, return_input_lines=False,
    return_damp=False):

    input_lines = []

    with open(mod_file) as input_data:
        for line in input_data:
            input_lines.append(line)

    input_data.close()


    depths = []
    vels = []
    sdepths = []
    svels = []
    damps = []
    sdamps = []

    nlayp = 0

    for i, line in enumerate(input_lines):
        line = line.strip().split()

        if i == 1 and line:
            nlayp = int(line[0])
        elif nlayp > 0 and i == nlayp + 2:
            nlays = int(line[0])
        else:
            pass

        if step:
            if i == 2 and line:
                depth = round(float(line[1]), 2)
                vel = round(float(line[0]), 2)
                damp = round(float(line[2]), 2)
                depths.append(depth)
                vels.append(vel)
                damps.append(damp)
            elif 3 <= i <= nlayp + 1 and line:
                depth = round(float(line[1]), 2)
                pline = input_lines[i - 1].strip().split()
                pvel = round(float(pline[0]), 2)
                vel = round(float(line[0]), 2)
                damp = round(float(line[2]), 2)
                depths.append(depth)
                depths.append(depth)
                vels.append(pvel)
                vels.append(vel)
                damps.append(damp)
                damps.append(damp)
            elif i == nlayp + 3 and line:
                sdepth = round(float(line[1]), 2)
                svel = round(float(line[0]), 2)
                sdamp = round(float(line[2]), 2)
                sdepths.append(sdepth)
                svels.append(svel)
                sdamps.append(sdamp)
            elif nlayp + 4 <= i <= nlayp + nlays + 3 and line:
                sdepth = round(float(line[1]), 2)
                spline = input_lines[i - 1].strip().split()
                spvel = round(float(spline[0]), 2)
                svel = round(float(line[0]), 2)
                sdamp = round(float(line[2]), 2)
                sdepths.append(sdepth)
                sdepths.append(sdepth)
                svels.append(spvel)
                svels.append(svel)
                sdamps.append(sdamp)
                sdamps.append(sdamp)
            else:
                pass
        else:
            if 2 <= i <= nlayp + 1 and line:
                depth = round(float(line[1]), 2)
                vel = round(float(line[0]), 2)
                damp = round(float(line[2]), 2)
                depths.append(depth)
                vels.append(vel)
                damps.append(damp)
            elif nlayp + 3 <= i <= nlayp + nlays + 3 and line:
                sdepth = round(float(line[1]), 2)
                svel = round(float(line[0]), 2)
                sdamp = round(float(line[2]), 2)
                sdepths.append(sdepth)
                svels.append(svel)
                sdamps.append(sdamp)
            else:
                pass

    # if sdepths and svels:
    #     if return_input_lines:
    #         return depths, vels, sdepths, svels, input_lines
    #     else:
    #         return depths, vels, sdepths, svels
    # else:
    #     if return_input_lines:
    #         return depths, vels, input_lines
    #     else:
    #         return depths, vels

    if return_input_lines and all((sdepths, svels)):
        if return_damp:
            return depths, vels, damps, sdepths, svels, sdamps, input_lines
        else:
            return depths, vels, sdepths, svels, input_lines
    elif not return_input_lines and all((sdepths, svels)):
        if return_damp:
            return depths, vels, damps, sdepths, svels, sdamps
        else:
            return depths, vels, sdepths, svels
    elif return_input_lines and not all((sdepths, svels)):
        if return_damp:
            return depths, vels, damps, input_lines
        else:
            return depths, vels, input_lines
    else:
        if return_damp:
            return depths, vels, damps
        else:
            return depths, vels

