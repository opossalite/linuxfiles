require("user")

local lazypath = vim.fn.stdpath('data') .. '/lazy/lazy.nvim'

-- Auto-install lazy.nvim if not present
if not vim.loop.fs_stat(lazypath) then
  print('Installing lazy.nvim....')
  vim.fn.system({
    'git',
    'clone',
    '--filter=blob:none',
    'https://github.com/folke/lazy.nvim.git',
    '--branch=stable', -- latest stable release
    lazypath,
  })
  print('Done.')
end

vim.opt.rtp:prepend(lazypath)


-- Lazy package manager installs
require('lazy').setup({

    -- LSP
    {'VonHeikemen/lsp-zero.nvim',
        branch = 'v2.x',
        dependencies = {
            -- LSP Support
            {'neovim/nvim-lspconfig'},             -- Required
            {                                      -- Optional
                'williamboman/mason.nvim',
                build = function()
                    pcall(vim.cmd, 'MasonUpdate')
                end,
            },
            {'williamboman/mason-lspconfig.nvim'}, -- Optional

            -- Autocompletion
            {'hrsh7th/nvim-cmp'},     -- Required
            {'hrsh7th/cmp-nvim-lsp'}, -- Required
            {'L3MON4D3/LuaSnip',       -- Required
                version = "v2.*",
                build = "make install_jsregexp"
            },
        }
    },
    {'nvim-treesitter/nvim-treesitter',
        build = ":TSUpdate",
        config = function()
            require("nvim-treesitter.configs").setup {
                --ensure_installed = { "c", "lua", "rust" },
                highlight = { enable = true, }
            }
        end
    },
    {'nvim-treesitter/playground'},
    --{'mrcjkb/haskell-tools.nvim',
    --    branch = '1.x.x',
    --    dependencies = {
    --        {'nvim-lua/plenary.nvim'},
    --        {'nvim-telescope/telescope.nvim'},
    --    }
    --},
    --{'mfussenegger/nvim-lint'},
    --{'mfussenegger/nvim-dap'},

    -- Tools
    {'nvim-telescope/telescope.nvim',
        tag = '0.1.5',
        dependencies = {
            {'nvim-lua/plenary.nvim'}
        }
    },
    {'theprimeagen/harpoon',
        branch = "master",
        dependencies = {
            {"nvim-lua/plenary.nvim"}
        }
    },
    {'windwp/nvim-autopairs',
        config = function() require('nvim-autopairs').setup{} end
    },
    {'voldikss/vim-floaterm'},
    --{'ptzz/lf.vim'},
    {'stevearc/aerial.nvim',
        attach_mode = "window",
    },
    --{'nvim-tree/nvim-tree.lua'},
    {'lambdalisue/fern.vim'},
    {'ggandor/leap.nvim',
        dependencies = {
            {'tpope/vim-repeat'}
        }
    },
    {'mfussenegger/nvim-jdtls'},

    -- Themes
    {'nvim-lualine/lualine.nvim',
        dependencies = {
            'nvim-tree/nvim-web-devicons'
        }
    },
    {'lukas-reineke/indent-blankline.nvim',
        main = "ibl",
        opts = {
            --scope = {
                --enabled = true,
                --highlight = { "SpecialKey", "SpecialKey", "SpecialKey" },
            --}
        }
    },
    --{'folke/styler.nvim',
    --    config = function()
    --        require("styler").setup {
    --            themes = {
    --                rust = {colorscheme = "ayu-mirage"},
    --                python = {colorscheme = "tokyonight-night"},
    --                haskell = {colorscheme = "tokyobones"},
    --                lua = {colorscheme = "catppuccin-mocha"},
    --            }
    --        }
    --    end
    --},
    {'folke/tokyonight.nvim', as = 'tokyonight'},
    {'catppuccin/nvim', as = 'catppuccin'},
    {'Mofiqul/dracula.nvim', as = 'dracula'},
    {'EdenEast/nightfox.nvim', as = 'nightfox'},
    {'rebelot/kanagawa.nvim', as = 'kanagawa'},
    {'rose-pine/neovim', as = 'rose-pine'},
    {'Shatur/neovim-ayu', as = 'ayu'},
    --{'navarasu/onedark.nvim', as = 'onedark'},
    {'marko-cerovac/material.nvim', as = 'material'},
    {'mcchrish/zenbones.nvim', as = 'zenbones',
        dependencies = {
            {'rktjmp/lush.nvim'}
        }
    },
    {'bluz71/vim-nightfly-colors', as = 'nightfly'},
    {'jacoborus/tender.vim', as = 'tender'},
    --{'NTBBloodbath/doom-one.nvim', as = 'doom-one'},
    --{'drewtempelmeyer/palenight.vim', as = 'palenight'},
    {'shaunsingh/moonlight.nvim', as = 'moonlight'},
    {'oxfist/night-owl.nvim', as = 'night-owl'},
    {'talha-akram/noctis.nvim', as = 'noctis'},
})



-- LSP setup
local lsp = require('lsp-zero').preset({})

lsp.on_attach(function(client, bufnr)
    lsp.default_keymaps({buffer = bufnr})
end)

lsp.on_attach(function(client, bufnr)
	local opts = {buffer = bufnr, remap = false}

	vim.keymap.set("n", "gd", function()
        vim.lsp.buf.definition()
    end, opts)
	vim.keymap.set("n", "K", function()
        vim.g.color_freeze = true
        vim.lsp.buf.hover()
    end, opts)
	--vim.keymap.set("n", "<leader>vk", function() vim.diagnostic.open_float() end, opts)
	vim.keymap.set("n", "N", function()
        vim.g.color_freeze = true
        vim.diagnostic.open_float()
    end, opts)
    vim.opt.signcolumn = "yes"
    client.server_capabilities.semanticTokensProvider = nil
end)

-- cmp setup
local cmp = require('cmp')
local cmp_action = require('lsp-zero').cmp_action()

cmp.setup({
  mapping = {
    -- `Enter` key to confirm completion
    --['<CR>'] = cmp.mapping.confirm({select = false}),
    ['<CR>'] = cmp.mapping(function(fallback) --disables the enter key
        fallback()
    end),

    -- Ctrl+Space to trigger completion menu
    ['<C-Space>'] = cmp.mapping.complete(),

    -- Navigate between snippet placeholder
    ['<C-f>'] = cmp_action.luasnip_jump_forward(),
    ['<C-b>'] = cmp_action.luasnip_jump_backward(),
  }
})


require('lspconfig').lua_ls.setup(lsp.nvim_lua_ls())
require'lspconfig'.hls.setup{}
require'lspconfig'.pyright.setup{}
require'lspconfig'.rust_analyzer.setup{}
require'lspconfig'.gopls.setup{}
require'lspconfig'.clangd.setup{}
require'lspconfig'.julials.setup{}
require'lspconfig'.zls.setup{}


lsp.setup()


