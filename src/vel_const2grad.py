#-*- coding: utf-8 -*-

import itertools
import time

import matplotlib.pyplot as plt
import numpy as np


st = list(time.localtime(time.time()))[0:-4]
timestamp = "{:04d}{:02d}{:02d}-{:02d}{:02d}".format(
    st[0], st[1], st[2], st[3], st[4])


colormap = ['#0067a7', '#bd1e24', '#007256', '#f6c700', '#964f8e',
    '#444444', '#e97600', '#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78',
    '#2ca02c', '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5',
    '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f', '#c7c7c7',
    '#bcbd22', '#dbdb8d', '#17becf', '#9edae5']


def extract_const(depths, velocities):
    vel_map = {}

    for i, depth in enumerate(depths, 1):
        if i < len(depths):
            ndepth = depths[i]
            vel = velocities[i - 1]

            for dd in np.arange(depth, ndepth, 0.1):
                dd = round(dd, 2)
                vel_map[dd] = vel

        elif i == len(depths):
            vel_map[depth] = velocities[i - 1]

        else:
            pass

    return vel_map

def return_gradient(new_depths, velocity_map):
    # Needs cleaning.
    grad_vels = []
    grad_depths = []

    depths = list(velocity_map)
    depth_min = min(depths)
    depth_max = max(depths)
    ndepth_min = min(new_depths)
    ndepth_max = max(new_depths)

    print(depths)

    if ndepth_min < depth_min:
        for dd in np.arange(int(ndepth_min), int(depth_min), 0.1):
            velocity_map[round(dd, 2)] = velocity_map[depth_min]
    else:
        pass

    if ndepth_max > depth_max:
        for dd in np.arange(int(depth_max), int(ndepth_max) + 1, 0.1):
            velocity_map[round(dd, 2)] = velocity_map[depth_max]
    else:
        pass

    dv_mod = []
    dd_mod = []

    for i, nwdepth in enumerate(new_depths):
        nwdepth = round(nwdepth, 2)
        # try with < and separate a case if i = 0 and nwdepth = 0.0
        if nwdepth <= 0.0 and i == 0:
        # if nwdepth <= 0.0 and i <= 1:
            # d0 = nwdepth
            # d1 = new_depths[i + 1]
            # v0 = velocity_map[d0]
            # v1 = (v0 + velocity_map[d1]) / 2.0
            # vm = v0
            # dm = (d0 + d1) / 2.0

            # k = (v1 - vm) / (d1 - dm)
            # n = vm - k * dm
            # vs = k * d0 + n

            # print(d0, d1, v0, v1, vm, dm, vs)

            grad_vels.append(velocity_map[nwdepth])
            # grad_vels.append(vs)
            grad_depths.append(nwdepth)

        # elif nwdepth == 0.0 and i == 0:
        #     d0 = nwdepth
        #     d1 = new_depths[i + 1]
        #     v0 = velocity_map[d0]
        #     v1 = (v0 + velocity_map[d1]) / 2.0
        #     vm = v0
        #     dm = (d0 + d1) / 2.0

        #     k = (v1 - vm) / (d1 - dm)
        #     n = vm - k * dm
        #     vs = k * d0 + n

        #     # print(d0, d1, v0, v1, vm, dm, vs)

        #     # grad_vels.append(velocity_map[nwdepth])
        #     grad_vels.append(vs)
        #     grad_depths.append(nwdepth)

        # elif nwdepth <= 0.0 and i == 1:
        # elif nwdepth <= 0.0 and i <= 2:
        elif nwdepth == 0.0 and i > 0:
            v0 = velocity_map[grad_depths[-1]]
            d1 = nwdepth
            v1 = velocity_map[nwdepth]

            v1 = (v0 + v1) / 2.0

            grad_vels.append(v1)
            grad_depths.append(d1)

        elif nwdepth > 0.0 and i == 0:
            pnwdepth = 0.0
            nnwdepth = new_depths[i + 1]

            vels_sel = []
            depths_sel = []

            for dd in np.arange(pnwdepth, nnwdepth, 0.1):
                vels_sel.append(velocity_map[dd])
                depths_sel.append(dd)

            avgvel = sum(vels_sel) / len(vels_sel)
            grad_vels.append(avgvel)
            grad_depths.append(nwdepth)

        # elif i == len(new_depths) - 2 and nwdepth == depth_max:
        #     grad_vels.append(velocity_map[depth_max])
        #     grad_depths.append(nwdepth)
        #     # print('Before last.')

        # elif nwdepth < depth_min:
        #     grad_vels.append(velocity_map[depth_min])
        #     grad_depths.append(nwdepth)
        #     # print('First.')

        elif nwdepth > depth_max:
        # elif nwdepth >= depth_max:
            grad_vels.append(velocity_map[depth_max])
            grad_depths.append(nwdepth)
            # print('Last.')

        else:
            d0 = new_depths[i - 1]
            v0 = grad_vels[-1]
            d1 = nwdepth
            dm = (d0 + d1) / 2.0

            avgvel = 0
            # tt = 0

            depth_int = np.arange(d0, d1, 0.1)

            for dd in depth_int:
                dd = round(dd, 2)
                avgvel += velocity_map[dd]
                # tt += 0.5 / velocity_map[dd]

            avgvel = avgvel / len(depth_int)

            k = (avgvel - v0) / (dm - d0)
            n = v0 - k * d0

            v1 = k * d1 + n
            # v1 = (2 * (d1 - d0) / tt) - v0

            if (v1 < velocity_map[d0] or v1 >= velocity_map[d1]) and v0 != avgvel:
                v1 = velocity_map[d1]
                # v1 = (avgvel + v1) / 2
                k = (v1 - v0) / (d1 - d0)
                n = v0 - k * d0
            # elif round(v0, 4) == round(avgvel, 4):
            # Is this elif block needed?
            elif round(velocity_map[d0], 4) == round(v1, 4):
                # v1o = v1
                vn = velocity_map[d1]
                v1 = (avgvel + vn) / 2
                k = (v1 - v0) / (d1 - d0)
                n = v0 - k * v0
                # print('OK!', d0, d1, vn, v1, v1o)
            else:
                pass

            # print('OK!', d0, d1, v1, avgvel)

            grad_depths.append(d1)
            grad_vels.append(v1)

            avgvel_grad = (v1 + v0) / 2.0

            dv = avgvel_grad - avgvel

            print(d0, d1, round(avgvel, 4), round(avgvel_grad, 4),
                round(dv, 4))

            dv_mod.append(dv)
            dd_mod.append(d1 - d0)

    adv_mod = np.absolute(dv_mod)
    avg_dv = sum(dv_mod) / len(dv_mod)
    aavg_dv = np.mean(adv_mod)
    wavg_dv = np.sum(np.array(dv_mod) * np.array(dd_mod)) / np.sum(dd_mod)
    waavg_dv = np.sum(np.array(adv_mod) * np.array(dd_mod)) / np.sum(dd_mod)

    print(round(avg_dv, 5), round(aavg_dv, 5), round(wavg_dv, 5),
        round(waavg_dv, 5))

    return grad_depths, grad_vels

def plot_choice(choice):
    if choice.lower() in ['vp', 'p', '']:
        # plt.xlabel(u'$v_P$ [km s$^{-1}$]', fontsize=12.0)
        plt.xlabel(u'$v_P$ [km/s]', fontsize=12.0)
        plot_name = "Constant layer $v_P$ model conversion"
        return "vp", plot_name
    elif choice.lower() in ['vs', 's']:
        # plt.xlabel(u'$v_s$ [km s$^{-1}$]', fontsize=12.0)
        plt.xlabel(u'$v_S$ [km/s]', fontsize=12.0)
        plot_name = "Constant layer $v_s$ model conversion"
        return "vs", plot_name
    elif choice.lower() in ['vpvs', 'vp/vs', 'vp vs']:
        plt.xlabel(u'$v_P$/$v_S$', fontsize=12.0)
        plot_name = "Constant layer $v_P$/$v_S$ model conversion"
        return "vpvs", plot_name
    else:
        print('Please specifiy correct option for plot type.')
        print('Possible choices: vp, vs, vpvs.')
        choice = input('\t> ')
        plot_choice(choice)

def plot_conversion(depths, velocities, gdepths, gvelocities, save_path=None,
    which='', labels=None):

    fig = plt.figure(figsize=(6.0, 12.0))
    ax = plt.subplot()

    # line, = plt.plot(velocities, depths, c='#0067a7',
    #     label='input constant velocity model', lw=0.75, alpha=0.7, zorder=8)
    # markers, = plt.plot(velocities, depths, c='#0067a7',
    #     label='input constant velocity model', lw=0.0, marker='D', ms=2.5,
    #     mfc='#0067a7', mec='k', mew=0.2, alpha=0.7, zorder=8)
    # legend_list.append((line, markers))

    app, plot_name = plot_choice(which)

    plt.plot(velocities, depths, c='0.4', lw=1.5, marker='D', ms=5.0,
        mfc='0.2', mec='k', mew=0.2, alpha=1.0, zorder=8,
        label='constant layer (MPS model)')

    if isinstance(gdepths[0], list):
        for i, gdl in enumerate(gdepths):
            if labels:
                plt.plot(gvelocities[i], gdl, c=colormap[i],
                    lw=1.75, alpha=0.9, zorder=8, label=labels[i])
            else:
                plt.plot(gvelocities[i], gdl, c=colormap[i],
                    lw=1.75, alpha=0.9, zorder=8, label='gradient')

        all_gvels = list(itertools.chain(*gvelocities))
        all_gdepths = list(itertools.chain(*gdepths))

    else:
        plt.plot(gvelocities, gdepths, c='#bd1e24', lw=1.75,
            alpha=0.7, zorder=8, label='gradient')

        all_gvels = gvelocities
        all_gdepths = gdepths

    all_vels = velocities + all_gvels
    all_depths = depths + all_gdepths

    min_vel = min(all_vels)
    max_vel = max(all_vels)
    min_depth = min(all_depths)
    # max_depth = max(all_depths)
    max_depth = max(depths)

    vel_range = max_vel - min_vel
    depth_range = max_depth - min_depth

    plt.xlim(min_vel - (vel_range * 0.25), max_vel + (vel_range * 0.25))
    # plt.xlim(5, 8.5)
    plt.ylim(max_depth + (depth_range * 0.05), min_depth - (depth_range * 0.05))

    if round(vel_range, 1) == 0.0:
        ax.set_aspect(0.15 / depth_range)
    else:
        ax.set_aspect( 2 * vel_range / depth_range)
        # ax.set_aspect( 5.0 / 70)

    plt.minorticks_on()
    # plt.grid(linestyle=(0,(10,5)), linewidth=0.3, color='0.7', zorder=-10)
    plt.yticks(fontsize=12.0)
    plt.xticks(fontsize=12.0)
    plt.grid(which='major', linestyle='solid', linewidth=0.5,
        color='0.5', alpha=0.5)

    plt.ylabel(u'depth [km]', fontsize=12.0)

    if save_path:
        save_path = \
            f"{save_path}_{timestamp}_velocity_model_conversion_{app}.png"
    else:
        save_path = f"{timestamp}_velocity_model_conversion_{app}.png"

    # plt.suptitle(plot_name, fontsize=10, horizontalalignment='center')
    ax.set_title(plot_name, fontsize=12.0, horizontalalignment='center')
    legend = ax.legend(title=None, fontsize=12.0, frameon=True, borderpad=1.0,
        labelspacing=0.6, borderaxespad=1.0, loc='best')
    legend.get_frame().set_linewidth(0.5)
    plt.savefig(
        save_path, dpi=300, facecolor='w', edgecolor='w',
        orientation='portrait', format=None, transparent=False,
        bbox_inches='tight', pad_inches=0.1,
        )
    plt.clf()
