-- If LuaRocks is installed, make sure that packages installed through it are
-- found (e.g. lgi). If LuaRocks is not installed, do nothing.
pcall(require, "luarocks.loader")

-- Standard awesome library
local gears = require("gears")
local awful = require("awful")
require("awful.autofocus")
-- Widget and layout library
local wibox = require("wibox")
-- Theme handling library
local beautiful = require("beautiful")
-- Notification library
local naughty = require("naughty")
local menubar = require("menubar")
local hotkeys_popup = require("awful.hotkeys_popup")
-- Enable hotkeys help widget for VIM and other apps
-- when client with a matching name is opened:
require("awful.hotkeys_popup.keys")

-- {{{ Error handling
-- Check if awesome encountered an error during startup and fell back to
-- another config (This code will only ever execute for the fallback config)
if awesome.startup_errors then
    naughty.notify({ preset = naughty.config.presets.critical,
                     title = "Oops, there were errors during startup!",
                     text = awesome.startup_errors })
end

-- Handle runtime errors after startup
do
    local in_error = false
    awesome.connect_signal("debug::error", function (err)
        -- Make sure we don't go into an endless error loop
        if in_error then return end
        in_error = true

        naughty.notify({ preset = naughty.config.presets.critical,
                         title = "Oops, an error happened!",
                         text = tostring(err) })
        in_error = false
    end)
end
-- }}}






--
-- CUSTOM FUNCTIONS
--

local function bind(keybind, func, description)
    awful.key(
        { table.unpack( keybind, 1, #keybind - 1 ) },
        keybind[#keybind],
        func,
        description

    )

    --awful.key({ modkey, }, "s",
    --    hotkeys_popup.show_help,
    --    {description = "show help", group="awesome"}),
end

function awful.util.fixed_indexing_filter(c, screen)
	if not c then
		return false
	end
	if not (c.skip_taskbar or c.hidden or c.type == "splash" or c.type == "dock" or c.type == "desktop") and awful.widget.tasklist.filter.currenttags(
		c,
		screen
	) then
		return true
	end
	return false
end

function awful.util.get_client_by_index(screen, i)
	local list = capi.client.get()

	local index = 0
	for _, c in ipairs(list) do
		if awful.util.fixed_indexing_filter(c, screen) then
			index = index + 1
			if (index == i) then
				return c
			end
		end
	end

	return nil
end

function awful.util.get_index_by_client(client)
	local screen = client.screen
	local list = capi.client.get()

	local index = 0
	for _, c in ipairs(list) do
		if awful.util.fixed_indexing_filter(c, screen) then
			index = index + 1
			if (c == client) then
				return index
			end
		end
	end
	return 1
end














-- {{{ Variable definitions
-- Themes define colours, icons, font and wallpapers.
--beautiful.init(gears.filesystem.get_themes_dir() .. "default/theme.lua")
local theme_path = string.format("%s/.config/awesome/themes/oni/theme.lua", os.getenv("HOME"), "zenburn")
beautiful.init(theme_path)

-- This is used later as the default terminal and editor to run.
terminal = "alacritty"
--editor = os.getenv("EDITOR") or "nano"
editor = "nvim"
editor_cmd = terminal .. " -e " .. editor

-- Default modkey.
-- Usually, Mod4 is the key with a logo between Control and Alt.
-- If you do not like this or do not have such a key,
-- I suggest you to remap Mod4 to another key using xmodmap or other tools.
-- However, you can use another modifier like Mod1, but it may interact with others.
modkey = "Mod4"
alt = "Mod1"

-- Table of layouts to cover with awful.layout.inc, order matters.
awful.layout.layouts = {
    awful.layout.suit.tile,
    awful.layout.suit.tile.left,
    awful.layout.suit.tile.bottom,
    awful.layout.suit.tile.top,
    awful.layout.suit.max,
    awful.layout.suit.floating,
    --awful.layout.suit.fair,
    --awful.layout.suit.fair.horizontal,
    --awful.layout.suit.spiral,
    --awful.layout.suit.spiral.dwindle,
    --awful.layout.suit.max.fullscreen,
    --awful.layout.suit.magnifier,
    --awful.layout.suit.corner.nw,
    -- awful.layout.suit.corner.ne,
    -- awful.layout.suit.corner.sw,
    -- awful.layout.suit.corner.se,
}
-- }}}

-- {{{ Menu
-- Create a launcher widget and a main menu
myawesomemenu = {
   { "hotkeys", function() hotkeys_popup.show_help(nil, awful.screen.focused()) end },
   { "manual", terminal .. " -e man awesome" },
   { "edit config", editor_cmd .. " " .. awesome.conffile },
   { "restart", awesome.restart },
   { "quit", function() awesome.quit() end },
}

mymainmenu = awful.menu({ items = { { "awesome", myawesomemenu, beautiful.awesome_icon },
                                    { "open terminal", terminal }
                                  }
                        })

mylauncher = awful.widget.launcher({ image = beautiful.awesome_icon,
                                     menu = mymainmenu })

-- Menubar configuration
menubar.utils.terminal = terminal -- Set the terminal for applications that require it
-- }}}

-- Keyboard map indicator and switcher
mykeyboardlayout = awful.widget.keyboardlayout()

-- {{{ Wibar
-- Create a textclock widget
mytextclock = wibox.widget.textclock()

-- Create a wibox for each screen and add it
local taglist_buttons = gears.table.join(
                    awful.button({ }, 1, function(t) t:view_only() end),
                    awful.button({ modkey }, 1, function(t)
                                              if client.focus then
                                                  client.focus:move_to_tag(t)
                                              end
                                          end),
                    awful.button({ }, 3, awful.tag.viewtoggle),
                    awful.button({ modkey }, 3, function(t)
                                              if client.focus then
                                                  client.focus:toggle_tag(t)
                                              end
                                          end),
                    awful.button({ }, 4, function(t) awful.tag.viewnext(t.screen) end),
                    awful.button({ }, 5, function(t) awful.tag.viewprev(t.screen) end)
                )

local tasklist_buttons = gears.table.join(
                     awful.button({ }, 1, function (c)
                                              if c == client.focus then
                                                  c.minimized = true
                                              else
                                                  c:emit_signal(
                                                      "request::activate",
                                                      "tasklist",
                                                      {raise = true}
                                                  )
                                              end
                                          end),
                     awful.button({ }, 3, function()
                                              awful.menu.client_list({ theme = { width = 250 } })
                                          end),
                     awful.button({ }, 4, function ()
                                              awful.client.focus.byidx(1)
                                          end),
                     awful.button({ }, 5, function ()
                                              awful.client.focus.byidx(-1)
                                          end))

local function set_wallpaper(s)
    ---- Wallpaper
    --if beautiful.wallpaper then
    --    local wallpaper = beautiful.wallpaper
    --    -- If wallpaper is a function, call it with the screen
    --    if type(wallpaper) == "function" then
    --        wallpaper = wallpaper(s)
    --    end
    --    gears.wallpaper.maximized(wallpaper, s, true)
    --end
    awful.spawn("nitrogen --restore")
end

-- Re-set wallpaper when a screen's geometry changes (e.g. different resolution)
screen.connect_signal("property::geometry", set_wallpaper)






-- generate a widget for the taglist with the cool line thingy, from here: https://github.com/nullchilly/nvim/
function tag_list(s)
	return awful.widget.taglist {
		screen = s,
		filter = awful.widget.taglist.filter.all,
		buttons = awful.util.table.join(
			awful.button({}, 1, function(t)
				t:view_only()
			end),
			awful.button({ modkey }, 1, function(t)
				if _G.client.focus then
					_G.client.focus:move_to_tag(t)
					t:view_only()
				end
			end),
			awful.button({}, 3, awful.tag.viewtoggle),
			awful.button({ modkey }, 3, function(t)
				if _G.client.focus then
					_G.client.focus:toggle_tag(t)
				end
			end),
			awful.button({}, 4, function(t)
				awful.tag.viewprev(t.screen)
			end),
			awful.button({}, 5, function(t)
				awful.tag.viewnext(t.screen)
			end)
		),
		style = {
            font = "monospace 11",
            spacing = 0,
			squares_sel = gears.surface.load_from_shape(
				beautiful.xresources.apply_dpi(30),
				beautiful.xresources.apply_dpi(26),
				gears.shape.transform(gears.shape.transform(gears.shape.rectangle))
                    : translate(0, 22),
				"#ff5555"
			),
			squares_sel_empty = gears.surface.load_from_shape(
				beautiful.xresources.apply_dpi(30),
				beautiful.xresources.apply_dpi(26),
				gears.shape.transform(gears.shape.rectangle)
                    : translate(0, 22),
				"#ff5555"
			),
			squares_unsel = gears.surface.load_from_shape(
				beautiful.xresources.apply_dpi(30),
				beautiful.xresources.apply_dpi(26),
				gears.shape.transform(gears.shape.rectangle)
                    : translate(0, 22),
				"#d2ffcf00"
			),
		},
		widget_template = {
			{
				{
					layout = wibox.layout.fixed.vertical,
					{
						{
							id = "text_role",
							widget = wibox.widget.textbox,
						},
						left = 6,
						right = 6,
						top = 2,
						bottom = 0,
						widget = wibox.container.margin,
					},
				},
				left = 2,
				right = 2,
				widget = wibox.container.margin,
			},
			id = "background_role",
			widget = wibox.container.background,
			shape = gears.shape.rectangle,
		},
	}
end





-- Toolbar, bottom bar
awful.screen.connect_for_each_screen(function(s)
    -- Wallpaper
    set_wallpaper(s)

    -- Each screen has its own tag table.
    awful.tag({ "1", "2", "3", "4", "5", "6", "7", "8", "9", "0" }, s, awful.layout.layouts[1])

    -- Create a promptbox for each screen
    s.mypromptbox = awful.widget.prompt()
    -- Create an imagebox widget which will contain an icon indicating which layout we're using.
    -- We need one layoutbox per screen.
    s.mylayoutbox = awful.widget.layoutbox(s)
    s.mylayoutbox:buttons(gears.table.join(
                           awful.button({ }, 1, function () awful.layout.inc( 1) end),
                           awful.button({ }, 3, function () awful.layout.inc(-1) end),
                           awful.button({ }, 4, function () awful.layout.inc( 1) end),
                           awful.button({ }, 5, function () awful.layout.inc(-1) end)))
    -- Create a taglist widget
    s.mytaglist = awful.widget.taglist {
        screen  = s,
        filter  = awful.widget.taglist.filter.all,
        buttons = taglist_buttons
    }

    -- Create a tasklist widget
    s.mytasklist = awful.widget.tasklist {
        screen  = s,
        filter  = awful.widget.tasklist.filter.currenttags,
        buttons = tasklist_buttons
    }

    -- Create the wibox
    s.mywibox = awful.wibar({ position = "bottom", screen = s, opacity = 1})





    -- Add widgets to the wibox
    s.mywibox:setup {
        layout = wibox.layout.align.horizontal,
        { -- Left widgets
            layout = wibox.layout.fixed.horizontal,
            --s.mytaglist,
            tag_list(s),
            s.mylayoutbox,
            s.mypromptbox,
        },
        s.mytasklist, -- Middle widget
        { -- Right widgets
            layout = wibox.layout.fixed.horizontal,
            mykeyboardlayout,
            wibox.widget.systray(),
            mytextclock,
            --mylauncher,
        }
    }
end)














-- }}}

-- {{{ Mouse bindings
root.buttons(gears.table.join(
    awful.button({ }, 3, function () mymainmenu:toggle() end),
    awful.button({ }, 4, awful.tag.viewnext),
    awful.button({ }, 5, awful.tag.viewprev)
))
-- }}}

-- {{{ Key bindings
globalkeys = gears.table.join(



    --
    -- Launch applications
    --

    -- terminal
    awful.key({ modkey }, "Return",
        function()
            awful.spawn(terminal)
        end,
        {description = "open a terminal", group = "launcher"}),

    -- dmenu
    awful.key({ modkey }, "space",
        function()
            awful.spawn("dmenu_run -nb '#282828' -sf '#FF5555' -sb '#464646' -nf '#bbbbbb'")
        end,
        {description = "open dmenu", group = "launcher"}),

    -- nemo
    awful.key({ modkey, alt }, "n",
        function()
            awful.spawn("nemo")
        end,
        {description = "open nemo", group = "launcher"}),

    -- firefox
    awful.key({ modkey, alt }, "f",
        function()
            awful.spawn("firefox")
        end,
        {description = "open firefox", group = "launcher"}),

    -- brave
    awful.key({ modkey, alt }, "b",
        function()
            awful.spawn("brave")
        end,
        {description = "open brave", group = "launcher"}),

    -- librewolf
    awful.key({ modkey, alt }, "l",
        function()
            awful.spawn("librewolf")
        end,
        {description = "open librewolf", group = "launcher"}),

    -- code
    awful.key({ modkey, alt }, "v",
        function()
            awful.spawn("code")
        end,
        {description = "open code", group = "launcher"}),

    -- discord
    awful.key({ modkey, alt }, "d",
        function()
            awful.spawn("discord")
        end,
        {description = "open discord", group = "launcher"}),

    -- lf
    awful.key({ modkey, alt }, "m",
        function()
            awful.spawn(terminal.." --command lf")
        end,
        {description = "open lf", group = "launcher"}),

    -- spotify
    awful.key({ modkey, alt }, "s",
        function()
            awful.spawn("spotify")
        end,
        {description = "open spotify", group = "launcher"}),

    -- steam
    awful.key({ modkey, alt }, "t",
        function()
            awful.spawn("steam")
        end,
        {description = "open steam", group = "launcher"}),



    --
    -- Restart applications
    --

    -- Restart Awesome (update config)
    awful.key({ modkey, "Shift" }, "r",
        awesome.restart,
        {description = "reload awesome", group = "awesome"}),

    -- nitrogen
    awful.key({ modkey, "Shift" }, "b",
        function()
            awful.spawn("nitrogen --restore")
        end,
        {description = "restart nitrogen", group = "launcher"}),

    -- polybar
    --awful.key({ modkey, "Shift" }, "p",
    --    function()
    --        awful.spawn("./.config/polybar/launch.sh $")
    --    end,
    --{description = "restart polybar", group = "launcher"}),



    --
    -- Lighting
    --

    -- enable night mode
    awful.key({ modkey }, "Prior",
        function()
            awful.spawn("redshift -P -O 2500")
        end,
        {description = "Enable night mode", group = "launcher"}),

    -- disable night mode
    awful.key({ modkey }, "Next",
        function()
            awful.spawn("redshift -P -O 6500")
        end,
        {description = "Disable night mode", group = "launcher"}),




    --
    -- Power
    --

    -- shutdown
    awful.key({ modkey }, "F1",
        function()
            awful.spawn("systemctl poweroff")
        end,
        {description = "shutdown", group = "launcher"}),

    -- restart
    awful.key({ modkey }, "F2",
        function()
            awful.spawn("systemctl reboot")
        end,
        {description = "restart", group = "launcher"}),

    -- Logout
    awful.key({ modkey }, "F3",
        awesome.quit,
        {description = "quit awesome", group = "awesome"}),



    --
    -- Workspaces
    --

    -- View previous
    --awful.key({ modkey }, "Left",
    --    awful.tag.viewprev,
    --    {description = "view previous", group = "tag"}),

    -- View next
    --awful.key({ modkey }, "Right",
    --    awful.tag.viewnext,
    --    {description = "view next", group = "tag"}),

    -- Focus next screen
    awful.key({ modkey }, "l",
        function()
            awful.screen.focus_relative( 1)
        end,
        {description = "focus the next screen", group = "screen"}),

    -- Focus last screen
    awful.key({ modkey}, "h",
        function()
            awful.screen.focus_relative(-1)
        end,
        {description = "focus the previous screen", group = "screen"}),

    -- Focus previous workspace
    --awful.key({ modkey }, "Escape",
    --    awful.tag.history.restore,
    --    {description = "go back", group = "tag"}),



    --
    -- Windows
    --

    -- Focus next
    awful.key({ modkey }, "j",
        function()
            awful.client.focus.byidx( 1)
        end,
        {description = "focus next by index", group = "client"}),

    -- Focus previous
    awful.key({ modkey }, "k",
        function()
            awful.client.focus.byidx(-1)
        end,
        {description = "focus previous by index", group = "client"}),

    -- Swap with next
    awful.key({ modkey, "Shift" }, "j",
        function()
            awful.client.swap.byidx(  1)
        end,
        {description = "swap with next client by index", group = "client"}),

    -- Swap with previous
    awful.key({ modkey, "Shift" }, "k",
        function()
            awful.client.swap.byidx( -1)
        end,
        {description = "swap with previous client by index", group = "client"}),

    -- Focus last
    --awful.key({ modkey }, "Tab",
    --    function()
    --        awful.client.focus.history.previous()
    --        if client.focus then
    --            client.focus:raise()
    --        end
    --    end,
    --    {description = "go back", group = "client"}),



    --
    -- Layouts
    --

    -- Increase master width
    awful.key({ modkey, "Control" }, "Right",
        function()
            awful.tag.incmwfact( 0.05)
        end,
        {description = "increase master width factor", group = "layout"}),

    -- Decrease master width
    awful.key({ modkey, "Control" }, "Left",
        function()
            awful.tag.incmwfact(-0.05)
        end,
        {description = "decrease master width factor", group = "layout"}),

    -- Increase # of master clients
    awful.key({ modkey, "Shift" }, "h",
        function()
            awful.tag.incnmaster( 1, nil, true)
        end,
        {description = "increase the number of master clients", group = "layout"}),

    -- Decrease # of master clients
    awful.key({ modkey, "Shift" }, "l",
        function()
            awful.tag.incnmaster(-1, nil, true)
        end,
        {description = "decrease the number of master clients", group = "layout"}),

    -- Increase # of columns
    awful.key({ modkey, "Control" }, "h",
        function()
            awful.tag.incncol( 1, nil, true)
        end,
        {description = "increase the number of columns", group = "layout"}),

    -- Decrease # of columns
    awful.key({ modkey, "Control" }, "l",
        function()
            awful.tag.incncol(-1, nil, true)
        end,
        {description = "decrease the number of columns", group = "layout"}),

    -- Select next layout
    awful.key({ modkey }, "Tab",
        function()
            awful.layout.inc( 1)
        end,
        {description = "select next", group = "layout"}),

    -- Select previous layout
    awful.key({ modkey, "Shift" }, "Tab",
        function()
            awful.layout.inc(-1)
        end,
        {description = "select previous", group = "layout"}),



    --
    -- Awesome
    --

    -- Help
    awful.key({ modkey, "Shift" }, "s",
        hotkeys_popup.show_help,
        {description = "show help", group="awesome"}),

    --bind({modkey, "s"}, 
--    hotkeys_popup.show_help,
    --    {description = "show help", group="awesome"}),

    -- Show main menu
    awful.key({ modkey }, "w",
        function()
            mymainmenu:show()
        end,
        {description = "show main menu", group = "awesome"}),

    -- Prompt
    awful.key({ modkey }, "r",
        function()
            awful.screen.focused().mypromptbox:run()
        end,
        {description = "run prompt", group = "launcher"}),

    -- Lua execute prompt
    awful.key({ modkey }, "x",
        function ()
            awful.prompt.run {
                prompt       = "Run Lua code: ",
                textbox      = awful.screen.focused().mypromptbox.widget,
                exe_callback = awful.util.eval,
                history_path = awful.util.get_cache_dir() .. "/history_eval"
            }
        end,
        {description = "lua execute prompt", group = "awesome"}),

    -- Menubar
    awful.key({ modkey }, "p",
        function()
            menubar.show()
        end,
        {description = "show the menubar", group = "launcher"}),



    --
    -- Unsure
    --

    -- Jump to urgent
    awful.key({ modkey }, "u",
        awful.client.urgent.jumpto,
        {description = "jump to urgent client", group = "client"}),

    -- Restore minimized
    awful.key({ modkey, "Shift" }, "n",
        function()
            local c = awful.client.restore()
            -- Focus restored client
            if c then
                c:emit_signal("request::activate", "key.unminimize", {raise = true})
            end
        end,
        {description = "restore minimized", group = "client"}),

    --
    awful.key({ modkey }, ";",
        function()
            awful.util.spawn_with_shell("sleep 0.075 && xdotool key U00F1")
        end,
        {description = "restart", group = "launcher"}),

    -- 
    awful.key({ modkey, "Shift" }, ";",
        function()
            awful.util.spawn_with_shell("sleep 0.075 && xdotool key Shift+U00F1")
        end,
        {description = "restart", group = "launcher"})

)

clientkeys = gears.table.join(

    -- Toggle fullscreen
    awful.key({ modkey }, "f",
        function(c)
            c.fullscreen = not c.fullscreen
            c:raise()
        end,
        {description = "toggle fullscreen", group = "client"}),

    -- Close window
    awful.key({ modkey, "Shift" }, "z",
        function (c) --also handle correct shift of focus
            c:kill()
        end,
        {description = "close", group = "client"}),

    -- Toggle floating
    awful.key({ modkey }, "s",
        awful.client.floating.toggle,
        {description = "toggle floating", group = "client"}),

    -- Move to master
    awful.key({ modkey, "Control" }, "Return",
        function(c)
            c:swap(awful.client.getmaster())
        end,
        {description = "move to master", group = "client"}),

    -- Move to screen
    awful.key({ modkey }, "o",
        function(c)
            c:move_to_screen()
        end,
        {description = "move to screen", group = "client"}),

    -- Toggle keep on top
    --awful.key({ modkey }, "t",
    --    function(c)
    --        c.ontop = not c.ontop
    --    end,
    --    {description = "toggle keep on top", group = "client"}),

    -- Minimize
    awful.key({ modkey }, "n",
        function (c)
            -- The client currently has the input focus, so it cannot be
            -- minimized, since minimized clients can't have the focus.
            c.minimized = true
        end,
        {description = "minimize", group = "client"}),

    -- Toggle maximize
    awful.key({ modkey }, "m",
        function (c)
            c.maximized = not c.maximized
            c:raise()
        end,
        {description = "(un)maximize", group = "client"})

    -- Toggle vertical maximize
    --awful.key({ modkey, "Control" }, "m",
    --    function (c)
    --        c.maximized_vertical = not c.maximized_vertical
    --        c:raise()
    --    end,
    --    {description = "(un)maximize vertically", group = "client"}),

    -- Toggle horizontal maximize
    --awful.key({ modkey, "Shift" }, "m",
    --    function (c)
    --        c.maximized_horizontal = not c.maximized_horizontal
    --        c:raise()
    --    end,
    --    {description = "(un)maximize horizontally", group = "client"})
)

-- Bind all key numbers to tags.
-- Be careful: we use keycodes to make it work on any keyboard layout.
-- This should map on the top row of your keyboard, usually 1 to 9.
for i = 1, 10 do
    globalkeys = gears.table.join(globalkeys,

        -- View tag only.
        awful.key({ modkey }, "#" .. i + 9,
            function()
                local screen = awful.screen.focused()
                local tag = screen.tags[i]
                if tag then
                    tag:view_only()
                end
            end,
            {description = "view tag #"..i, group = "tag"}),


        -- Move client to tag.
        awful.key({ modkey, "Shift" }, "#" .. i + 9,
            function()
                if client.focus then
                    local tag = client.focus.screen.tags[i]
                    if tag then
                        client.focus:move_to_tag(tag)
                    end
                end
            end,
            {description = "move focused client to tag #"..i, group = "tag"}),


        -- Move client to tag and view.
        awful.key({ modkey, "Control" }, "#" .. i + 9,
            function()

                if client.focus then
                    local screen = awful.screen.focused()
                    local tag = screen.tags[i]
                    local tag = client.focus.screen.tags[i]
                    if tag then
                        client.focus:move_to_tag(tag)
                        tag:view_only()
                    end
                end

                --if client.focus then
                --    local tag = client.focus.screen.tags[i]
                --    if tag then
                --        client.focus:move_to_tag(tag)
                --    end
                --end


                --local screen = awful.screen.focused()
                --local tag = screen.tags[i]
                --if tag then
                --    tag:view_only()
                --end
            end,
            {description = "move focused client to tag #"..i, group = "tag"})


        -- Toggle tag display.
        --awful.key({ modkey, "Control" }, "#" .. i + 9,
        --    function ()
        --        local screen = awful.screen.focused()
        --        local tag = screen.tags[i]
        --        if tag then
        --            awful.tag.viewtoggle(tag)
        --        end
        --    end,
        --    {description = "toggle tag #" .. i, group = "tag"}),


        -- Toggle tag on focused client.
        --awful.key({ modkey, "Control", "Shift" }, "#" .. i + 9,
        --    function ()
        --        if client.focus then
        --            local tag = client.focus.screen.tags[i]
        --            if tag then
        --                client.focus:toggle_tag(tag)
        --            end
        --        end
        --    end,
        --    {description = "toggle focused client on tag #" .. i, group = "tag"})
    )
end

clientbuttons = gears.table.join(
    awful.button({ }, 1, function (c)
        c:emit_signal("request::activate", "mouse_click", {raise = true})
    end),
    awful.button({ modkey }, 1, function (c)
        c:emit_signal("request::activate", "mouse_click", {raise = true})
        awful.mouse.client.move(c)
    end),
    awful.button({ modkey }, 3, function (c)
        c:emit_signal("request::activate", "mouse_click", {raise = true})
        awful.mouse.client.resize(c)
    end)
)

-- Set keys
root.keys(globalkeys)
-- }}}

-- {{{ Rules
-- Rules to apply to new clients (through the "manage" signal).
awful.rules.rules = {
    -- All clients will match this rule.
    { rule = { },
      properties = { border_width = beautiful.border_width,
                     border_color = beautiful.border_normal,
                     focus = awful.client.focus.filter,
                     raise = true,
                     keys = clientkeys,
                     buttons = clientbuttons,
                     screen = awful.screen.preferred,
                     placement = awful.placement.no_overlap+awful.placement.no_offscreen
     }
    },

    -- Floating clients.
    { rule_any = {
        instance = {
          "DTA",  -- Firefox addon DownThemAll.
          "copyq",  -- Includes session name in class.
          "pinentry",
        },
        class = {
          "Arandr",
          "Blueman-manager",
          "Gpick",
          "Kruler",
          "MessageWin",  -- kalarm.
          "Sxiv",
          "Tor Browser", -- Needs a fixed window size to avoid fingerprinting by screen size.
          "Wpa_gui",
          "veromix",
          "xtightvncviewer"},

        -- Note that the name property shown in xprop might be set slightly after creation of the client
        -- and the name shown there might not match defined rules here.
        name = {
          "Event Tester",  -- xev.
        },
        role = {
          "AlarmWindow",  -- Thunderbird's calendar.
          "ConfigManager",  -- Thunderbird's about:config.
          "pop-up",       -- e.g. Google Chrome's (detached) Developer Tools.
        }
      }, properties = { floating = true }},

    -- Add titlebars to normal clients and dialogs
    { rule_any = {type = { "normal", "dialog" }
      }, properties = { titlebars_enabled = false }
    },

    -- Set Firefox to always map on the tag named "2" on screen 1.
    -- { rule = { class = "Firefox" },
    --   properties = { screen = 1, tag = "2" } },

    -- Code to screen 1 workspace 1
    { rule = { class = "code-oss" },
        properties = { screen = 1, tag = "1" }},

    -- Discord to screen 2 workspace 8
    { rule = { class = "discord" },
        properties = { screen = 2, tag = "8" }},

    -- Spotify to screen 2 workspace 9
    { rule = { class = "Spotify" },
        properties = { screen = 2, tag = "9" }},

}
-- }}}

-- {{{ Signals

-- Make Spotify follow its specific rules
client.connect_signal("manage", function (c)
    if c.class == nil then
        c.minimized = true
        c:connect_signal("property::class", function ()
            c.minimized = false
            awful.rules.apply(c)
        end)
    end
end)

-- Make new windows spawn as slaves
client.connect_signal("manage", function(c)
    -- Similar behavior as other window managers DWM, XMonad.
    -- Master-Slave layout new client goes to the slave, master is kept
    -- If you need new slave as master press: ctrl + super + return
    if not awesome.startup then awful.client.setslave(c) end
end)

-- Signal function to execute when a new client appears.
--client.connect_signal("manage", function (c)
--    -- Set the windows at the slave,
--    -- i.e. put it at the end of others instead of setting it master.
--    -- if not awesome.startup then awful.client.setslave(c) end
--
--    if awesome.startup
--      and not c.size_hints.user_position
--      and not c.size_hints.program_position then
--        -- Prevent clients from being unreachable after screen count changes.
--        awful.placement.no_offscreen(c)
--    end
--end)

-- Add a titlebar if titlebars_enabled is set to true in the rules.
client.connect_signal("request::titlebars", function(c)
    -- buttons for the titlebar
    local buttons = gears.table.join(
        awful.button({ }, 1, function()
            c:emit_signal("request::activate", "titlebar", {raise = true})
            awful.mouse.client.move(c)
        end),
        awful.button({ }, 3, function()
            c:emit_signal("request::activate", "titlebar", {raise = true})
            awful.mouse.client.resize(c)
        end)
    )

    awful.titlebar(c) : setup {
        { -- Left
            awful.titlebar.widget.iconwidget(c),
            buttons = buttons,
            layout  = wibox.layout.fixed.horizontal
        },
        { -- Middle
            { -- Title
                align  = "center",
                widget = awful.titlebar.widget.titlewidget(c)
            },
            buttons = buttons,
            layout  = wibox.layout.flex.horizontal
        },
        { -- Right
            awful.titlebar.widget.floatingbutton (c),
            awful.titlebar.widget.maximizedbutton(c),
            awful.titlebar.widget.stickybutton   (c),
            awful.titlebar.widget.ontopbutton    (c),
            awful.titlebar.widget.closebutton    (c),
            layout = wibox.layout.fixed.horizontal()
        },
        layout = wibox.layout.align.horizontal
    }
end)

-- Enable sloppy focus, so that focus follows mouse.
client.connect_signal("mouse::enter", function(c)
    c:emit_signal("request::activate", "mouse_enter", {raise = false})
end)

client.connect_signal("focus", function(c) c.border_color = beautiful.border_focus end)
client.connect_signal("unfocus", function(c) c.border_color = beautiful.border_normal end)
-- }}}

awful.util.spawn_with_shell("~/.autorun")
