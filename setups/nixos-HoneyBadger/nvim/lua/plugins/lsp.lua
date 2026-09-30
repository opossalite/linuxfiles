return {
  {
    "williamboman/mason.nvim",
    build = ":MasonUpdate",
    opts = {
      ui = { border = "rounded" },
    },
  },
  {
    "neovim/nvim-lspconfig",
    dependencies = {
      "mason.nvim",
      "williamboman/mason-lspconfig.nvim",
      "saghen/blink.cmp",
    },
    config = function()
      -- Advertise blink.cmp's completion capabilities to every server.
      local capabilities = require("blink.cmp").get_lsp_capabilities()
      vim.lsp.config("*", { capabilities = capabilities })

      -- lua_ls needs a bit of extra config so it understands the Neovim API.
      vim.lsp.config("lua_ls", {
        settings = {
          Lua = {
            diagnostics = { globals = { "vim" } },
            workspace = { checkThirdParty = false },
            telemetry = { enable = false },
          },
        },
      })

      require("mason-lspconfig").setup({
        -- Language servers to guarantee are installed. Covers Lua (for this
        -- config itself), Python, JS/TS, Bash, Rust, Go, and C/C++.
        ensure_installed = {
          "lua_ls",
          "pyright",
          "ts_ls",
          "bashls",
          "rust_analyzer",
          "gopls",
          "clangd",
        },
        -- Any OTHER server you manually :MasonInstall also gets auto-installed
        -- again on future startups, and Neovim will offer to install a server
        -- automatically the first time you open a filetype it covers.
        automatic_installation = true,
        -- Neovim 0.11+: calls vim.lsp.enable() for each installed server for you,
        -- picking up the configs (and the "*" capabilities) set above.
        automatic_enable = true,
      })

      -- Keymaps that apply once an LSP attaches to a buffer.
      vim.api.nvim_create_autocmd("LspAttach", {
        group = vim.api.nvim_create_augroup("UserLspAttach", { clear = true }),
        callback = function(event)
          local map = function(mode, lhs, rhs, desc)
            vim.keymap.set(mode, lhs, rhs, { buffer = event.buf, desc = desc })
          end
          map("n", "gd", vim.lsp.buf.definition, "Goto definition")
          map("n", "gD", vim.lsp.buf.declaration, "Goto declaration")
          map("n", "gr", vim.lsp.buf.references, "Goto references")
          map("n", "gI", vim.lsp.buf.implementation, "Goto implementation")
          map("n", "K", vim.lsp.buf.hover, "Hover docs (type info, etc.)")
          map("n", "<leader>rn", vim.lsp.buf.rename, "Rename symbol")
          map({ "n", "v" }, "<leader>ca", vim.lsp.buf.code_action, "Code action")
        end,
      })
    end,
  },
}
