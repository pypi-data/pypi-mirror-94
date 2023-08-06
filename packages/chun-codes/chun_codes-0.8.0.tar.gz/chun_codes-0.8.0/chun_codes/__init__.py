import sys

import time
from datetime import datetime as dt

import numpy as np

import matplotlib.pyplot as plt
from matplotlib import gridspec
from matplotlib.backends.backend_pdf import PdfPages

from astropy import log

py_vers = sys.version_info.major
if py_vers == 2:
    import pdfmerge

__version__ = "0.8.0"


def systime():
    return time.strftime("%d_%b_%Y_%H:%M:%S", time.localtime())


class TimerClass:
    """
    Purpose:
      Object that records elapsed time

    Attributes
    ----------
    start : datetime object
            Starting value for timer
    stop  : datetime object
            Stopping value for timer
    delta : datetime object
            Time difference
    """

    def __init__(self):
        self.start = 0
        self.stop = 0
        self.delta = 0
        self.format = ""

    def _start(self):
        self.start = dt.now()

    def _stop(self):
        self.stop = dt.now()
        self.delta = self.stop - self.start
        sec = self.delta.seconds
        HH = sec // 3600
        MM = (sec // 60) - (HH * 60)
        SS = sec - (HH * 3600) - (MM * 60)
        self.format = "%i hours  %i minutes  %i seconds" % (HH, MM, SS)


def match_nosort(a, b, unique=False):
    # Modified on 06/04/2016 to include unique.

    subb = np.repeat(-1, len(a))

    for ii in range(len(a)):
        mark = np.where(b == a[ii])
        if len(mark[0]) == 1:
            subb[ii] = mark[0]
        if len(mark[0]) >= 2:
            if unique:
                subb[ii] = mark[0][0]

    suba = (np.where(subb != -1))[0]
    subb = subb[suba]

    return suba, subb


def match_nosort_str(a, b):
    # Not fully tested

    sub_b = np.repeat(-1, len(a))

    # sub_a = np.array([i for i, v in enumerate(a) if v in set(b)])

    for ii in range(len(a)):
        mark = [xx for xx in range(len(b)) if a[ii] in b[xx]]
        if len(mark) == 1:
            sub_b[ii] = mark[0]

    sub_a = (np.where(sub_b != -1))[0]
    sub_b = sub_b[sub_a]

    return sub_a, sub_b


def intersect(a, b):
    """
    Purpose:
      Find the common intersection of two list using set logic

    :param a: first list or numpy array
    :param b: second list or numpy array
    :return: numpy array containing intersection of values
    """
    return np.array(list(set(a) & set(b)))


def intersect_ndim(a, b, shape0):
    """
    Similar to intersect to cross-match multi-dimensional indexing arrays
    Uses numpy unravel and ravel options

    Parameters
    ----------
    a : tuple containing numpy arrays for each dimension.
        Output of np.where() calls

    b : tuple containing numpy arrays for each dimension.
        Output of np.where() calls

    shape0 : tuple or list
        Shape of N-dimensional numpy array. e.g., [array].shape

    Returns
    -------
    tuple containing numpy arrays for each dimension
    """

    ravel_a = np.ravel_multi_index(a, shape0)
    ravel_b = np.ravel_multi_index(b, shape0)
    ab_union = intersect(ravel_a, ravel_b)
    if len(ab_union) != 0:
        return np.unravel_index(ab_union, shape0)
    else:
        return [-1]


def chun_crossmatch(x1, y1, x2, y2, dcr, silent=False, verbose=False, sph=False):
    # Mod on 23/04/2016 to fix ind1,ind2 if no return is made

    if not silent:
        print('### Begin chun_crossmatch ' + systime())

    len0 = len(x1)

    cnt = 0
    for ii in range(len0):
        if verbose and len0 >= 100000:
            if ii % 1000 == 0:
                print('ii = %s %s'.format(ii, systime()))

        if sph:
            x_diff = (x1[ii] - x2) * 3600.0 * np.cos(y1[ii] * np.pi / 180.0)
            y_diff = (y1[ii] - y2) * 3600.0
        else:
            x_diff = x1[ii] - x2
            y_diff = y1[ii] - y2

        distance = np.sqrt(x_diff ** 2 + y_diff ** 2)

        in_reg = (np.where(distance <= dcr))[0]

        if len(in_reg) > 0:
            min0 = [xx for xx in range(len(distance)) if
                    (distance[xx] == np.min(distance[in_reg]))]
            if cnt == 0:
                save = min0
                z_save = [ii]
                dx = [x_diff[min0]]
                dy = [y_diff[min0]]
            else:
                z_save.append(ii)

                if len(min0) == 1:
                    save.append(min0[0])
                    dx.append(x_diff[min0])
                    dy.append(y_diff[min0])
                else:
                    for jj in range(len(min0)):
                        save.append(min0[jj])
                        dx.append(x_diff[min0[jj]])
                        dy.append(y_diff[min0[jj]])
            cnt = cnt + 1

    if cnt == 0:
        ind1 = np.array([-1])
        ind2 = np.array([-1])
    else:
        ind1 = np.array(z_save)
        ind2 = np.array(save)

    if not silent:
        print('### End chun_crossmatch ' + systime())
    return ind1, ind2


def ds9_reg(XX, YY, ds9_file, color='green', aperture=[2.0], image=False, wcs=False, file0=''):
    if color != 'green':
        color_str = ' # color = ' + color
    else:
        color_str = ''

    if not image and not wcs:
        print("Error. Require image or wcs flag")
        return

    if image:
        coord = 'physical'
        suffix0 = ')' + color_str

    if wcs:
        coord = 'fk5'
        suffix0 = '")' + color_str

    if len(aperture) == 1:
        aperture0 = np.repeat(aperture[0], len(XX))
    else:
        aperture0 = aperture

    str0 = ['# Region file format: DS9 version 4.0', '# Filename: ' + file0,
            ' global color=green font="helvetica 10 normal" select=1 ' +
            'highlite=1 edit=1 move=1 delete=1 include=1 fixed=0 source', coord]

    print('### Writing : ', ds9_file)
    f = open(ds9_file, 'w')
    for jj in range(len(str0)): f.write(str0[jj] + '\n')
    for ii in range(len(XX)):
        txt = 'circle(%f,%f,%f%s\n' % (XX[ii], YY[ii], aperture0[ii], suffix0)
        f.write(txt)

    f.close()


def random_pdf(x, dx, seed_i=False, n_iter=1000, silent=True):
    """
    Created on 24/06/2016
    Modified on 29/06/2016 to reverse shape
    """

    len0 = len(x)
    if not silent:
        print(len0)

    # Mod on 29/06/2016
    x_pdf = np.zeros((len0, n_iter), dtype=np.float64)
    # x_pdf = np.zeros((n_iter, len0), dtype=np.float64)

    if seed_i:
        seed0 = seed_i + np.arange(len0)

    for ii in range(len0):
        if not seed_i:
            temp = np.random.normal(0.0, 1.0, size=n_iter)
        else:
            np.random.seed(seed0[ii])
            temp = np.random.normal(0.0, 1.0, size=n_iter)

        rand_ans = x[ii] + dx[ii] * temp
        x_pdf[ii] = rand_ans

    return x_pdf


def compute_onesig_pdf(arr0, x_val, usepeak=False, silent=True, verbose=False):
    """
    Created on 28/06/2016
    Modified on 29/06/2016 to handle change in shape
    """

    if not silent:
        print('### Begin compute_onesig_pdf | ' + systime())

    len0 = arr0.shape[0]  # arr0.shape[1] # Mod on 29/06/2016

    err = np.zeros((len0, 2))  # np.zeros((2,len0)) # Mod on 29/06/2016
    x_peak = np.zeros(len0)

    for ii in range(len0):
        test = arr0[ii]  # arr0[:,ii] # Mod on 29/06/2016
        good = np.where(np.isfinite(test))[0]
        if len(good) > 0:
            v_low = np.percentile(test[good], 15.8655)
            v_high = np.percentile(test[good], 84.1345)

            x_peak[ii] = np.percentile(test[good], 50.0)
            if not usepeak:
                t_ref = x_val[ii]
            else:
                t_ref = x_peak[ii]

            err[ii, 0] = t_ref - v_low
            err[ii, 1] = v_high - t_ref
    if not silent:
        print('### End compute_onesig_pdf | ' + systime())
    return err, x_peak


def plot_data_err_hist(x, dx, x_label, out_pdf, c0='b', m0='o', a0=0.5, s0=25,
                       x_bins=50, y_bins=50, xlim=None, ylim=None):
    """

    Generate plot of variable and uncertainty on variable. This produces
    a three-panel PDF with histograms on variable at the bottom and
    uncertainty on the right side (oriented 90deg)

    Parameters
    ----------
    x : array_like
      An array or arrays of variable (N or N_var x N)

    dx : array_like
      An array or arrays of uncertainty for x (N or N_var x N)

    x_label: str
      Label for x

    out_pdf : file path, file object, or file like object
      File to write to.  If opened, must be opened for append (ab+).

    c0 : color or sequence of color, optional, default : 'b'
      `c` can be a single color format string, or a sequence of color
      specifications of length `N`, or a sequence of `N` numbers to be
      mapped to colors using the `cmap` and `norm` specified via kwargs
      (see below). Note that `c` should not be a single numeric RGB or
      RGBA sequence because that is indistinguishable from an array of
      values to be colormapped.  `c` can be a 2-D array in which the
      rows are RGB or RGBA, however.

    m0 : `~matplotlib.markers.MarkerStyle`, optional, default: 'o'
      See `~matplotlib.markers` for more information on the different
      styles of markers scatter supports.

    a0 : scalar, optional, default: None
      The alpha blending value, between 0 (transparent) and 1 (opaque)

    s0 : int
      Size of markers

    x_bins : integer or array_like for x, optional, default: 50
      If an integer is given, `bins + 1` bin edges are returned,
      consistently with :func:`numpy.histogram` for numpy version >= 1.3.

    y_bins : integer or array_like for dx, optional, default: 50
      If an integer is given, `bins + 1` bin edges are returned,
      consistently with :func:`numpy.histogram` for numpy version >= 1.3.

    xlim : array_like, optional, default: None
        limits for x

    ylim : array_like, optional, default: None
        limits for dx

    Notes
    -----
        Created by Chun Ly on 29 June 2016
        Additional modification to handle multiple variables
    """

    if x.ndim == 1:
        x = x.reshape((1, len(x)))
        dx = dx.reshape((1, len(dx)))
        x_label = [x_label]
        xlim = np.array(xlim)
        xlim = xlim.reshape((1, 2))
        ylim = np.array(ylim)
        ylim = ylim.reshape((1, 2))

    n_var = x.shape[0]

    pp = PdfPages(out_pdf)

    for ii in range(n_var):
        gs = gridspec.GridSpec(3, 3)
        ax1 = plt.subplot(gs[:-1, :-1])
        ax2 = plt.subplot(gs[2, :-1])
        ax3 = plt.subplot(gs[:-1, 2])

        # Panel 1

        # Get number of sources within region
        if not isinstance(xlim, type(None)) and not isinstance(ylim, type(None)):
            in_field = [(xlim[ii, 0] <= a <= xlim[ii, 1] and
                         ylim[ii, 0] <= b <= ylim[ii, 1]) for a, b in
                        zip(x[ii], dx[ii])]

        ax1_label = 'N=' + str(sum(in_field))
        ax1.scatter(x[ii], dx[ii], c=c0, marker=m0, s=s0, alpha=a0,
                    edgecolor='none', label=ax1_label)
        ax1.xaxis.set_ticklabels([])

        if not isinstance(xlim, type(None)):
            ax1.set_xlim(xlim[ii])
        if not isinstance(ylim, type(None)):
            ax1.set_ylim(ylim[ii])

        ylabel = r'$\sigma$(' + x_label[ii] + ')'
        ax1.set_ylabel(ylabel)

        ax1.legend(loc='lower right', fontsize='12', scatterpoints=3,
                   frameon=False)

        # Lower histogram
        ax2.hist(x[ii], bins=x_bins, fc=c0, alpha=a0, histtype='stepfilled',
                 edgecolor='None')
        ax2.hist(x[ii], bins=x_bins, fc='None', histtype='stepfilled',
                 edgecolor=c0, lw=1.5)

        avg0 = '%.3f ' % np.average(x[ii])
        med0 = '%.3f ' % np.median(x[ii])
        sig0 = '%.3f ' % np.std(x[ii])
        txt0 = 'Average : ' + avg0 + '\n' + 'Median : ' + med0 + '\n' + r'$\sigma$ : ' + sig0
        ax2.annotate(txt0, (0.97, 0.97), xycoords='axes fraction', ha='right',
                     va='top')

        ax2.set_xlabel(x_label[ii])
        ax2.set_ylabel('N')

        if not isinstance(xlim, type(None)):
            ax2.set_xlim(xlim[ii])
        else:
            ax2.set_xlim(ax1.get_xlim())

        # Right histogram
        ax3.hist(dx[ii], bins=y_bins, orientation='horizontal', fc=c0, alpha=a0,
                 histtype='stepfilled', edgecolor='None')
        ax3.hist(dx[ii], bins=y_bins, orientation='horizontal', fc='None',
                 histtype='stepfilled', edgecolor=c0, lw=1.5)
        ax3.yaxis.set_ticklabels([])

        ax3.set_xlabel('N')

        avg0 = '%.3f ' % np.average(dx[ii])
        med0 = '%.3f ' % np.median(dx[ii])
        txt0 = 'Average : ' + avg0 + '\n' + 'Median : ' + med0
        ax3.annotate(txt0, (0.94, 0.03), xycoords='axes fraction',
                     ha='right', va='bottom')

        if not isinstance(ylim, type(None)):
            ax3.set_ylim(ylim[ii])
        else:
            ax3.set_ylim = (ax1.get_ylim())

        # Tick marks
        ax1.minorticks_on()
        ax2.minorticks_on()
        ax3.minorticks_on()

        plt.subplots_adjust(left=0.01, bottom=0.01, top=0.99, right=0.99,
                            wspace=0.05, hspace=0.05)

        fig = plt.gcf()
        fig.set_size_inches(8, 8)

        fig.savefig(pp, format='pdf', bbox_inches='tight')
        plt.close()
        fig.clear()

    print('### Writing : ', out_pdf)
    pp.close()


def quad_low_high_err(err, hi=None):

    if isinstance(hi, type(None)):
        return np.sqrt((err[:, 0] ** 2 + err[:, 1] ** 2) / 2.0)
    else:
        return np.sqrt((err ** 2 + hi ** 2) / 2.0)


def plot_compare(x0, y0, out_pdf, labels, extra_label=['', ''], idx=None,
                 x0_err=None, y0_err=None, xlim=None, ylim=None, c0='b',
                 m0='o', a0=0.5, s0=25, silent=False, verbose=True):
    """
    Provide explanation for function here.

    Parameters
    ----------
    x0 : array_like
        An array or arrays of variable (N or N_var x N)

    y0 : array_like
        An array or arrays of variable (N or N_var x N)

    out_pdf : file path, file object, or file like object
        File to write to.  If opened, must be opened for append (ab+).

    labels : string array
        An array or labeling for x- and y-axes with dimension of N_var

    extra_label : string array (optional)
        Additional string to append to labels for x- (1st entry) and
        y- (2nd entry) axes

    idx : array like
        Indexing array for sources to determine determine average, median.
        This allows you to exclude NaNs or unavailable values.
        Default: All sources included

    x0_err : array_like
        An array or arrays of uncertainty for x0 (N or N_var x N)

    y0_err : array_like
        An array or arrays of uncertainty for y0 (N or N_var x N)

    xlim : array_like, optional, default: None
        limits for upper panel (x0 vs y0)

    ylim : array_like, optional, default: None
        y-limit for lower panel (difference)

    c0 : color or sequence of color, optional, default : 'b'
        `c` can be a single color format string, or a sequence of color
        specifications of length `N`, or a sequence of `N` numbers to be
        mapped to colors using the `cmap` and `norm` specified via kwargs
        (see below). Note that `c` should not be a single numeric RGB or
        RGBA sequence because that is indistinguishable from an array of
        values to be colormapped.  `c` can be a 2-D array in which the
        rows are RGB or RGBA, however.

    m0 : `~matplotlib.markers.MarkerStyle`, optional, default: 'o'
        See `~matplotlib.markers` for more information on the different
        styles of markers scatter supports.

    a0 : scalar, optional, default: 0.5
        The alpha blending value, between 0 (transparent) and 1 (opaque)

    s0 : scalar or array_like, shape (n, ), optional, default: 25
        size in points^2.

    silent : boolean
          Turns off stdout messages. Default: False

    verbose : boolean
          Turns off additional stdout messages. Default: True

    Returns
    -------

    Notes
    -----
    Created by Chun Ly, 15 July 2016
    Modified by Chun Ly, 18 July 2016
     - Minor modification for limit for [in_field]
    """

    if not silent:
        print('### Begin plot_compare | ' + systime())

    if x0.ndim == 1:
        x0 = x0.reshape((1, len(x0)))
        y0 = y0.reshape((1, len(y0)))
        if not isinstance(xlim, type(None)):
            xlim = np.array(xlim)
            xlim = xlim.reshape((1, 2))
        if not isinstance(ylim, type(None)):
            ylim = np.array(ylim)
            ylim = ylim.reshape((1, 2))

    n_var = x0.shape[0]

    if isinstance(idx, type(None)):
        idx = range(x0.shape[1])

    pp = PdfPages(out_pdf)

    for ii in range(n_var):
        gs = gridspec.GridSpec(2, 1, height_ratios=[3, 1])
        ax1 = plt.subplot(gs[0])
        ax2 = plt.subplot(gs[1])

        # Top Panel #

        # Get number of sources within region
        if not isinstance(xlim, type(None)) and not isinstance(ylim, type(None)):
            # Mod on 18/07/2016. Bug found with y range. ylim -> xlim
            in_field = [(xlim[ii, 0] <= a <= xlim[ii, 1] and
                         xlim[ii, 0] <= b <= xlim[ii, 1]) for a, b in
                        zip(x0[ii], y0[ii])]

            ax1_label = 'N=' + str(sum(in_field))

        ax1.plot(xlim[ii], xlim[ii], 'r--')

        ax1.scatter(x0[ii], y0[ii], c=c0, marker=m0, s=s0, alpha=a0,
                    edgecolor='none', label=ax1_label)

        ax1.xaxis.set_ticklabels([])

        if not isinstance(xlim, type(None)):
            ax1.set_xlim(xlim[ii])
            ax1.set_ylim(xlim[ii])

        ylabel = labels[ii] + extra_label[1]  # ' (re-derived)'
        ax1.set_ylabel(ylabel)

        ax1.legend(loc='lower right', fontsize='12', scatterpoints=3,
                   frameon=False)

        # Bottom Panel #

        ax2.plot(xlim[ii], [0, 0], 'r--')

        diff0 = y0[ii] - x0[ii]
        ax2.scatter(x0[ii], diff0, c=c0, marker=m0, s=s0, alpha=a0,
                    edgecolor='none')

        avg0 = '%.3f ' % np.average(diff0[idx])
        med0 = '%.3f ' % np.median(diff0[idx])
        sig0 = '%.3f ' % np.std(diff0[idx])
        txt0 = 'Average : ' + avg0 + '\n' + 'Median : ' + med0 + '\n' + r'$\sigma$ : ' + sig0
        ax2.annotate(txt0, (0.97, 0.97), xycoords='axes fraction', ha='right',
                     va='top')

        xlabel = labels[ii] + extra_label[0]  # ' (published)'
        ax2.set_xlabel(xlabel)
        ax2.set_ylabel('diff.')

        if not isinstance(xlim, type(None)):
            ax2.set_xlim(xlim[ii])
        else:
            ax2.set_xlim(ax1.get_xlim())

        if not isinstance(ylim, type(None)):
            ax2.set_ylim(ylim[ii])

        ax1.minorticks_on()
        ax2.minorticks_on()

        plt.subplots_adjust(left=0.01, bottom=0.01, top=0.99, right=0.99,
                            wspace=0.03, hspace=0.03)

        fig = plt.gcf()
        fig.set_size_inches(8, 8)

        fig.savefig(pp, format='pdf', bbox_inches='tight')
        plt.close()
        fig.clear()

    print('### Writing : ', out_pdf)
    pp.close()

    if not silent:
        print('### End plot_compare | ' + systime())


def rem_dup(values):
    """
    Purpose:
      Remove duplicates in a list

    :param values: list
    :return: numpy array containing non-duplicate arrays
    """

    output = []
    seen = set()
    for value in values:
        if value not in seen:
            output.append(value)
            seen.add(value)
    return np.array(output)


def gauss2d(xy, amplitude, xo, yo, sigma_x, sigma_y, theta, offset):
    """
    Purpose:
      This function provides a 2-D Gaussian for scipy's opt.curve_fit()

    Parameters
    ----------
    xy : tuple
       Tuple of x,y grid from numpy.meshgrid()
       gx = np.linspace(0,shape0[0]-1,shape0[0])
       gy = np.linspace(0,shape0[1]-1,shape0[1])
       gx, gy = numpy.meshgrid(gx, gy)
       xy = (gx, gy)

    amplitude : float
      Peak of Gaussian

    xo : float
      Gaussian center value along x

    yo : float
      Gaussian center value along y

    sigma_x : float
      Gaussian sigma along x

    sigma_y : float
      Gaussian sigma along y

    theta : float
      Orientation along major axis of Gaussian. Positive is clock-wise.

    offset : float
      Level of continuum

    Returns
    -------
    g.ravel() : numpy.ndarray
      Contiguous flattened array

    Notes
    -----
    Created by Chun Ly, 26 April 2017
     - Copied from MMTtools.mmtcam for more general use
    Modified by Chun Ly, 6 May 2017
     - Fix bug. Need to import numpy
    """

    x = xy[0]
    y = xy[1]

    xo = np.array(xo)
    yo = np.array(yo)
    a = (np.cos(theta) ** 2) / (2 * sigma_x ** 2) + (np.sin(theta) ** 2) / (2 * sigma_y ** 2)
    b = -(np.sin(2 * theta)) / (4 * sigma_x ** 2) + (np.sin(2 * theta)) / (4 * sigma_y ** 2)
    c = (np.sin(theta) ** 2) / (2 * sigma_x ** 2) + (np.cos(theta) ** 2) / (2 * sigma_y ** 2)
    g = offset + amplitude * np.exp(- (a * ((x - xo) ** 2) + 2 * b * (x - xo) * (y - yo)
                                       + c * ((y - yo) ** 2)))
    return g.ravel()


def exec_pdfmerge(files, pages, outfile, merge=False, silent=False):
    """
    Purpose:
      Executes pdfmerge (2.7x compatiable) command to grab necessary pages
      and merge them if desired

    Require installing pdfmerge:
    https://pypi.python.org/pypi/pdfmerge/0.0.7
      > pip install pdfmerge

    :param files: list
      List of files (must include full path)
    :param pages: list
      List of strings indicating pages to extract.
      E.g.: ['4,6,15,20','3,8,44,50']
    :param outfile: list or str
      Either List of files to write or a single file if merge == True
    :param merge: bool
      Indicate whether to merge into a single file, [outfile]
    :param silent: bool
      Indicate whether to silence messages

    Notes
    -----
    Created by Chun Ly, 22 January 2018
    """

    if py_vers != 2:
        version_full = sys.version.split(' ')[0]
        log.warning("exec_pdfmerge: Incompatible with python %s" % version_full)
        raise SystemError("Incompatible with python %s" % version_full)

    if not merge:
        if len(outfile) != len(files):
            log.warn('### outfile input not complete. Missing files!')

    if not silent:
        log.info('### Begin exec_pdfmerge : ' + systime())

    n_files = len(files)

    writer0 = None

    for nn in range(n_files):
        writer0 = pdfmerge.add(files[nn], rules=pages[nn], writer=writer0)

        if not merge:
            with open(outfile[nn], 'wb') as stream:
                writer0.write(stream)
            writer0 = None

    if merge:
        with open(outfile, 'wb') as stream:
            writer0.write(stream)

    if not silent:
        log.info('### End exec_pdfmerge : ' + systime())
