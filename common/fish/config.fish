set -gx EDITOR nvim

#set -gx QT_AUTO_SCREEN_SET_FACTOR 0
#set -gx QT_SCALE_FACTOR 2
#set -gx QT_FONT_DPI 144

#set -gx GDK_SCALE 2
#set -gx GDK_DPI_SCALE 0.5

if status is-interactive
    # Commands to run in interactive sessions can go here


    ###########
    # STARTUP #
    ###########


    # clear greeting
    set fish_greeting ""

    # run fastfetch if enough horizontal space
    if [ (tput cols) -ge 77 ] #tput lines
	fastfetch -l openSUSE
    end







    #############
    # VARIABLES #
    #############


    #set -gx EDITOR="nvim"







    #############
    # FUNCTIONS #
    #############


    # simple miscellaneous
    #function cp
	    #command cp -i
	#end
    function whereami
        command pwd
    end

    # ls variations
    function ls
        command ls --color=auto $argv
    end
    function la
        command ls --color=auto -a $argv
    end
    function ll
        command ls --color=auto -l $argv
    end


    # home-manager variations
    function he
        command home-manager edit
    end
    function hs
        command home-manager switch
    end


    # git variations
    function gitconfigp
        command git config user.name opossalite
        command git config user.email werbird10@gmail.com
    end
    function gitconfigw
        command git config user.name nbalcarc
        command git config user.email nathan.balcarcel@gmail.com
    end
    function gitconfigh
        command git config user.name horprus
        command git config user.email horprus@proton.me
    end


    # python
    function py
        python $argv
    end
    function pyv
        set VENVPATH {$HOME}"/venvs/"{$argv[1]}
        if test -d $VENVPATH
            source {$VENVPATH}"/bin/activate.fish"
        else
            echo "Could not find virtual environment"
        end
    end
    function da
        deactivate
    end


end

set -q GHCUP_INSTALL_BASE_PREFIX[1]; or set GHCUP_INSTALL_BASE_PREFIX $HOME ; set -gx PATH $HOME/.cabal/bin /home/terrior/.ghcup/bin $PATH # ghcup-env
