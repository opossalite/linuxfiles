return {
  "nvim-neo-tree/neo-tree.nvim",
  branch = "v3.x",
  dependencies = {
    "nvim-lua/plenary.nvim",
    "nvim-tree/nvim-web-devicons",
    "MunifTanjim/nui.nvim",
  },
  cmd = "Neotree",
  keys = {
    { "<leader>e", "<cmd>Neotree toggle<CR>", desc = "Toggle file tree" },
    { "<leader>f", "<cmd>Neotree toggle<CR>", desc = "Toggle file tree" },
  },
  opts = {
    close_if_last_window = true,
    window = {
      position = "left",
      width = 32,
      mappings =  {
        ["l"] = "open",
      },
    },
    filesystem = {
      follow_current_file = { enabled = true },
      use_libuv_file_watcher = true, -- live-updates the tree on external changes
      filtered_items = {
        visible = false,
        hide_dotfiles = false,
        hide_gitignored = false,
      },
    },
  },
}
