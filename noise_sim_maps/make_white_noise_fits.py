
import os
import numpy as np
import astropy.units as u
from astropy.wcs import WCS
try:
    import tolteca.simu.toltec.sim_fits_class as t
except ImportError as ie:
    # Sounds like tolteca wasn't installed
    # or it wasn't installed in this environment
    raise ie

if __name__ == "__main__":

    # center of the fits file
    ra_center = 92.0
    dec_center = -7.0

    # random seed
    seed = 6

    # pixel size (can't/don't change this plz)
    pixel_size = 1.0 * u.arcsecond
    CDELT      = pixel_size.to(u.degree).value # degree
    
    # size of the map
    NAXIS1_length     = 5 * u.arcminute
    NAXIS2_length     = 5 * u.arcminute
    NAXIS1 = int((NAXIS1_length / pixel_size).cgs.value)
    NAXIS2 = int((NAXIS2_length / pixel_size).cgs.value)

    # generate white noise maps
    rng = np.random.default_rng(seed)
    
    # only put it in the 1100_I, 1400_I, 2000_U hdus
    flux = 100 # in units MJy / sr
    imgs = 9 * [None]
    imgs[0] = rng.random([NAXIS1, NAXIS2]) * flux
    imgs[3] = rng.random([NAXIS1, NAXIS2]) * flux
    imgs[6] = rng.random([NAXIS1, NAXIS2]) * flux
    
    # wcs information
    wcs_input_dict = {
        'CTYPE1': 'RA---TAN',
        'CUNIT1': 'deg',
        'CDELT1': -CDELT,
        'CRPIX1': int(NAXIS1 / 2),
        'CRVAL1': ra_center,
        'NAXIS1': NAXIS1,
        'CTYPE2': 'DEC--TAN',
        'CUNIT2': 'deg',
        'CDELT2': CDELT,
        'CRPIX2': int(NAXIS2/2),
        'CRVAL2': dec_center,
        'NAXIS2': NAXIS2
    }
    wcs_dict = WCS(wcs_input_dict)
    header = wcs_dict.to_header(relax=True)

    # so we know
    other_meta = {
        'RND_SEED': seed
    }

    sf = t.sim_fits()
    sf.generate_fits(imgs=imgs, wcs=wcs_dict, convolve_img=True, **other_meta)

    sf.raw_hdul.writeto(f'{seed}_raw_white_noise.fits',
        output_verify='exception', overwrite=True, checksum=True)

    sf.convolved_hdul.writeto(f'{seed}_convolved_white_noise.fits',
        output_verify='exception', overwrite=True, checksum=True)
    
    print(f'Convolution corresponds to a {t.toltec_beams().toltec_fwhm} arcsec beams respectively')