function ColorMyPencils(color)
	--color = color or "ayu-mirage"
    color = color or "catppuccin"
	vim.cmd.colorscheme(color)

	vim.api.nvim_set_hl(0, "Normal", { bg = "none" })
	vim.api.nvim_set_hl(0, "NormalFloat", { bg = "none" })
end

require('rose-pine').setup({
    variant = "moon", --main, moon, dawn
    disable_background = false,
})
require('catppuccin').setup({
    flavour = "macchiato", --latte, frappe, macchiato, mocha
})
require('kanagawa').setup({
    theme = "lotus", --wave, dragon, lotus
})

ColorMyPencils()
