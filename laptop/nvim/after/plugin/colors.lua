vim.opt.termguicolors = true

require('rose-pine').setup({
    variant = "moon", --main, moon, dawn	
})
require('catppuccin').setup({
    flavour = "macchiato", --latte, frappe, macchiato, mocha
})
require('kanagawa').setup({
    theme = "lotus", --wave, dragon, lotus
})
require('ayu').setup({
    mirage = false, -- Set to `true` to use `mirage` variant instead of `dark` for dark background.
    overrides = {}, -- A dictionary of group names, each associated with a dictionary of parameters (`bg`, `fg`, `sp` and `style`) and colors in hex.
})

-- Apply theme and disable background
vim.cmd.colorscheme('ayu-mirage')
vim.api.nvim_set_hl(0, "Normal", {bg = "none"})
vim.api.nvim_set_hl(0, "NormalFloat", {bg = "none"})

