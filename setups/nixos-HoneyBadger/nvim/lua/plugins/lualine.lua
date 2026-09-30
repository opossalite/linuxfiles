return {
  "nvim-lualine/lualine.nvim",
  dependencies = { "nvim-tree/nvim-web-devicons" },
  event = "VeryLazy",
  opts = {
    options = {
      theme = "gruvbox",
      globalstatus = true,
      component_separators = { left = "│", right = "│" },
      section_separators = { left = "", right = "" },
    },
    sections = {
      lualine_a = { "mode" },
      lualine_b = { "branch", "diff" },
      lualine_c = { { "filename", path = 1 } },
      -- Diagnostic counts (errors/warnings) shown right on the bar.
      lualine_x = { "diagnostics", "encoding", "filetype" },
      lualine_y = { "progress" },
      lualine_z = { "location" },
    },
  },
}
