return {
  "ellisonleao/gruvbox.nvim",
  priority = 1000, -- load before other plugins so highlight groups exist
  lazy = false,
  config = function()
    require("gruvbox").setup({
      contrast = "hard", -- "hard", "soft", or "" for default
      terminal_colors = true,
    })
    vim.cmd.colorscheme("gruvbox")
  end,
}
