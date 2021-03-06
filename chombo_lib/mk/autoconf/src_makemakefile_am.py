#
# $(top_srcdir)/bootstrap runs this in each directory under lib/src, to
# produce an appropriate Makefile.am.
#

import glob
import sys
import os
import string
import chombo_utils
from chombo_utils import echo_n


if __name__ == '__main__':
    
    print '#******************************************************************#'
    print '# Do not edit this file.  It was generated by                      #'
    print '# lib/mk/autoconf/src_makemakefile_am.py.                          #'
    print '#******************************************************************#'
    
    min_spacedim =  int( sys.argv[1] )
    max_spacedim =  int( sys.argv[2] )

    has_chf = (len(glob.glob('*.ChF')) > 0)
    has_cpp = (len(glob.glob('*.cpp')) > 0)
    has_H   = (len(glob.glob('*.H')) > 0)
    has_f   = (len(glob.glob('*.f')) > 0)
    
    #
    # Generate Makefile.am in lib/src/*/multidim directory.
    #
    if os.path.basename( os.getcwd() ) == 'multidim':
        if os.path.exists( './extern.list' ):
            print 'EXTRA_DIST = dim-independent-headers.txt extern.list makefile.anag'
        else:
            print 'EXTRA_DIST = dim-independent-headers.txt             makefile.anag'

        print ".PHONY: install-data-hook"
        print 'install-data-hook:'
        print '\t$(top_srcdir)/lib/util/multidim/make_headers.sh $(srcdir) $(pkgincludedir) $(CH_MIN_SPACEDIM) $(CH_MAX_SPACEDIM)'
        sys.exit( 0 )


    #
    # This has to go before the "if MULTIDIM_ONLY_AM" or automake isn't happy.
    #
    print 'include $(top_srcdir)/lib/mk/autoconf/Automake.rules'

    if os.path.exists('./multidim'):
        print 'DIST_SUBDIRS = multidim'
        print "if MULTIDIM_ONLY_AM"
        print "  SUBDIRS = multidim"
        print "else"
        print "if MULTIDIM_AM"
        print "  SUBDIRS = multidim"
        print "endif MULTIDIM_AM"
        # The "endif" goes at the very bottom of the Makefile.am; we don't want to
        # do anything *but* go into the multidim subdirectory, if !MULTIDIM_ONLY_AM.
        # I'd like to go into the multidim subdir only once, but the
        # problem with that is that I can change a header and its multidim
        # versions don't get reinstalled!


    #
    # nodist_fort_HEADERS
    #
    generated_F_headers = []
    if has_chf:
      echo_n( 'nodist_fort_HEADERS = ' )
      for f in glob.glob('*.ChF'):
        stump=f.split('.')[0]
        echo_n( stump + '_F.H ' )
        generated_F_headers.append( stump + '_F.H' )
      print ''
      print 'fortdir = $(pkgincludedir)'
    
    #
    # GENERATED_FORTRAN
    #
    generated_f_files = []
    echo_n( 'GENERATED_FORTRAN = ' )
    if has_chf:
      for f in glob.glob( '*.ChF' ):
        stump=f.split('.')[0]
        echo_n( stump + '.f ' )
        generated_f_files.append( stump + '.f' )
      print ''
      print ''
    print ''

    echo_n( "RAW_FORTRAN = " )
    if has_f:
      for f in glob.glob('*.f'):
        if not f in generated_f_files:
            echo_n( str(f) + ' ' )
    print ""
    print 'CLEANFILES = $(MOSTLYCLEANFILES) ' + string.join(generated_f_files) \
          + ' ' + string.join(generated_F_headers)

    #
    # CPP files
    #
    print 'if !SMALLBUILD_AM'
    echo_n( 'CPP_FILES = ' )
    if has_cpp:
      for f in glob.glob( '*.cpp' ):
        echo_n( f + ' ' )
      print ''
    print ''
    print 'endif !SMALLBUILD_AM'
    
    #
    # library
    # 
    normalized_dirname=os.path.basename( os.getcwd() ).lower()
    for dim in range( min_spacedim, max_spacedim+1 ):
        echo_n ( 'if CH_' + str(dim) + 'D\n' )
        echo_n( '  ' + normalized_dirname + str(dim) + 'D_LTLIBRARIES = lib'
            + normalized_dirname + str(dim) + 'D.la' + '\n' )
        echo_n( '  nodist_lib' + normalized_dirname + str(dim) + 'D_la_SOURCES '
            + '= $(GENERATED_FORTRAN) $(CPP_FILES) $(RAW_FORTRAN)' + '\n' )
        print ''
        echo_n( '  ' + normalized_dirname + str(dim) + 'Ddir = $(pkglibdir)\n' )
        echo_n( 'endif CH_' + str(dim) + 'D' + '\n')

        #
        # It would be nice to avoid this "if CH_2D, if CH_3D" stuff, but automake doesn't
        # let me define a target with a variable in it, e.g.
        # nodist_libboxtools$(DIM)D_LTLIBRARIES.
        #

    curdir = os.path.basename( os.getcwd() )
    sys.stdout.write( 'AM_LDFLAGS += '
                     + chombo_utils.getAM_LDFLAGS(curdir, src_test='src')
                     + '\n' )

    # Install headers, if any.  (Regular, unidim headers.  Multidim headers
    # are installed elsewhere.)
    if has_H:
        echo_n( 'headers_HEADERS = $(srcdir)/*.H\n' )
        echo_n( 'headersdir = $(pkgincludedir)\n' )

    
    echo_n( 'EXTRA_DIST += ' )
    if has_chf:
      echo_n( '*.ChF ' )
    if has_cpp:
      echo_n( '*.cpp ' )
    print ''
    
    #
    # FortranNameMacro.H, if we're in BoxTools
    #
    if (normalized_dirname == 'smallboxtools') or (normalized_dirname == 'boxtools'):
      print "BUILT_SOURCES = FortranNameMacro.H"
      print "FortranNameMacro.H :"
      print '\t$(top_srcdir)/lib/util/multidim/make_FortranNameMacro_H.sh > $(srcdir)/FortranNameMacro.H'

    if os.path.isfile('MakefileAm.extra') : print 'include $(srcdir)/MakefileAm.extra'    
    
    # Matching endif from way almost the beginning of the Makefile.am:
    if os.path.exists('./multidim'):
      print 'endif !MULTIDIM_ONLY_AM'
