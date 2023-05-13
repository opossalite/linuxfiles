-- Theme settings
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
vim.api.nvim_set_hl(0, "Normal", {bg = "none"})
vim.api.nvim_set_hl(0, "NormalFloat", {bg = "none"})
vim.cmd.colorscheme('rose-pine')

