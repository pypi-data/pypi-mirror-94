#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import warnings
import HMpTy

def read_tilefile(filename, **kwargs):
    """ reads the tilefile and returns a pandas.DataFrame """
    extension = filename.split(".")[-1]

    # = Fits pandas reader
    if extension == "fits":
        from astropy.io import fits
        from astropy.table import Table

        t_ = Table(fits.getdata(filename, **kwargs) )
        
        try:
            dataframe = t_.to_pandas()
        except ValueError:
            # remove multi-dimentional columns
            t_.remove_columns([col for col in t_.colnames if len(t_[col].shape)>1])
            dataframe = t_.to_pandas()

    # Hoping it exists
    else: 
        dataframe = getattr("pandas.read_{extension}")(filename, **kwargs)

    return dataframe

class HTMQuery( object ):
    
    def __init__(self, depth=7, directory=None):
        """ """
        self._htm  = HMpTy.HTM(depth)

        self.set_directory(directory)

    def set_directory(self, directory):
        """ """
        self._directory = directory
    
    def get_htmtiles(self, ra, dec, radius, **kwargs):
        """ get the name of the HTM tiles (tixels) intesecting with the given 'cone'
        
        Parameters
        ----------
        ra, dec: [float, float]
             coordinates in degree.

        radius: [float]
             size of the radius search (in degree)
             
        Returns
        -------
        list if tile ids
        """
        return self.htm.intersect(ra,dec, radius)

    def fetch_cat_htmtiles(self, ra, dec, radius, directory=None, extension=".fits", **kwargs):
        """ get the catalog file overlapping with the given 'cone'

        Parameters
        ----------
        ra, dec: [float, float]
            coordinates in degree.

        radius: [float]
            size of the radius search (in degree)
             

        directory: [str] -optional-
            Localtion of the `tile.fits` files
            = requested if set_directory() has not be called or directory not in initialisation = 

        extension: [str] -optional-
            extension of the fimes. 
            = 

        Returns
        -------
        list if tile ids
        """
        tiles = self.get_htmtiles(ra, dec, radius, **kwargs)
        if directory is None:
            directory = self.directory

        if directory is None:
            raise ValueError("You must provide the catalog directory, provide as an option or set it using set_directory()")
        
        filepath = []
        for tile_ in tiles:
            filename = os.path.join(directory, str(tile_)+extension)
            if not os.path.isfile(filename):
                warnings.warn(f"{tile_} not found in {directory} ; (looked for {filename})")
            else:
                filepath.append(filename)
                
        return filepath

    def fetch_cat(self, ra, dec, radius, directory=None, ext=None, **kwargs):
        """ """
        import pandas

        if directory is None:
            directory = self.directory

        if directory is None:
            raise ValueError("You must provide the catalog directory, provide as an option or set it using set_directory()")
        
        filepath = self.fetch_cat_htmtiles(ra, dec, radius, directory=directory, **kwargs)
        tiles = [os.path.basename(file_).split(".")[0] for file_ in filepath]
        dataframes = [read_tilefile(file_) for file_ in filepath]
            
        return pandas.concat(dataframes, keys=tiles)
        
        
    # =============== #
    #  Properties     #
    # =============== #
    @property
    def htm(self):
        """  """
        return self._htm

    
    @property
    def directory(self):
        """  """
        if not hasattr(self, "_directory"):
            self._directory = None
        return self._directory
        
