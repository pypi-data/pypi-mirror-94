import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

def pseudoslit(data, pa, width=1, precision=100, ax=None):
    dims = len(data.shape)
    if dims==2:
        a, b = data.shape
    else:
        a, b, vel_size = data.shape
    data_prec = np.repeat(np.repeat(data, precision, axis=0), precision, axis=1)
    templ = np.zeros((a*precision, b*precision))
    phi = np.radians(pa-90)
    slope, interc = np.tan(phi), np.abs(width/(2*np.cos(phi)))*precision

    yy, xx = np.mgrid[0:a*precision, 0:b*precision]
    yy_data, xx_data = np.mgrid[0:a, 0:b]
    y1 = interc + xx[0]*slope + a*precision/2*(1-slope)
    y2 = -interc + xx[0]*slope + a*precision/2*(1-slope)
    templ[[(yy<y1)&(yy>y2)][0]] = 1

    Rxx = (xx - b/2*precision)*np.cos(-phi) - (yy - a/2*precision)*np.sin(-phi)
    Ryy = (xx - b/2*precision)*np.sin(-phi) + (yy - a/2*precision)*np.cos(-phi)
    
    if ax is not None:
        im = ax.imshow(Rxx)
        divider = make_axes_locatable(ax)
        cax = divider.append_axes('right', size='10%', pad=0.1)
        fig.colorbar(im, cax=cax, orientation='vertical')
    
    r, result = [], []  
    row_yy = (Ryy<width/2*precision)&(Ryy>-width/2*precision)
       
    for j in range(-int(a/2**0.5)-1, int(a/2**0.5)+1):
        square = (Rxx>j*precision)&(Rxx<(j+1)*precision)&(row_yy)
        if dims == 2: 
            res_w = np.sum(data_prec[yy[square], xx[square]], axis=0)
            if (res_w!=0.) and (np.sum(square)>0.99*width*precision**2):         
                r.append(j)
                result.append(res_w/np.sum(square))
                if ax is not None:
                    ax.plot(xx[square], yy[square], 'ro', markersize=0.1, color=[(j+a)/(2*a),1,0])
        else: 
            res_w = np.sum(data_prec[yy[square], xx[square], :], axis=0)
            if (np.max(res_w)>0) and (np.sum(square)>0.99*width*precision**2):         
                r.append(j)
                result.append(res_w/np.sum(res_w))
                if ax is not None:
                    ax.plot(xx[square], yy[square], 'ro', markersize=0.1, color=[(j+a)/(2*a),1,0])
                
    if dims == 2:
        return np.array(r), np.array(result)        
    else:
        return np.array(r), np.rot90(np.array(result), k=-1)