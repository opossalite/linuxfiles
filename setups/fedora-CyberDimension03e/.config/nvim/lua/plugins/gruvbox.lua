return {
  -- add gruvbox
  { "ellisonleao/gruvbox.nvim" },

  -- Configure LazyVim to load gruvbox
  {
    "LazyVim/LazyVim",
    priority = 1000,
    config = true,
    opts = {
      colorscheme = "gruvbox",
    },
  },
}
