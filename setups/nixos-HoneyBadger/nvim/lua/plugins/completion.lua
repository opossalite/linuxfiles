return {
  "saghen/blink.cmp",
  version = "*", -- use a tagged release (prebuilt binary, no Rust toolchain needed)
  dependencies = { "rafamadriz/friendly-snippets" },
  event = "InsertEnter",
  opts = {
    keymap = {
      preset = "none", -- don't use a preset that binds <CR>
      ["<C-y>"] = { "select_and_accept" },
      ["<C-n>"] = { "select_next", "fallback" },
      ["<C-p>"] = { "select_prev", "fallback" },
      ["<Tab>"] = { "select_next", "fallback" },
      ["<S-Tab>"] = { "select_prev", "fallback" },
      ["<C-space>"] = { "show", "show_documentation", "hide_documentation" },
      ["<C-e>"] = { "hide" },
    },
    appearance = {
      nerd_font_variant = "mono",
    },
    completion = {
      documentation = { auto_show = true, auto_show_delay_ms = 200 },
      menu = { border = "rounded" },
      ghost_text = { enabled = true }, -- inline preview of the top suggestion
    },
    sources = {
      default = { "lsp", "path", "snippets", "buffer" },
    },
    signature = { enabled = true, window = { border = "rounded" } },
  },
  opts_extend = { "sources.default" },
}
