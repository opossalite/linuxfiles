local rainbow = require 'ts-rainbow'
vim.api.nvim_set_hl(0, 'TSRainbowYellow', {fg = '#ffd700'})
vim.api.nvim_set_hl(0, 'TSRainbowMagenta', {fg = '#da70d6'})
vim.api.nvim_set_hl(0, 'TSRainbowBlue', {fg = '#179fff'})

require'nvim-treesitter.configs'.setup {
    -- A list of parser names, or "all" (the four listed parsers should always be installed)
    ensure_installed = { "c", "lua", "vim", "help", "cpp", "rust", "python", "javascript", "typescript" },

    -- Install parsers synchronously (only applied to `ensure_installed`)
    sync_install = false,

    -- Automatically install missing parsers when entering buffer
    -- Recommendation: set to false if you don't have `tree-sitter` CLI installed locally
    auto_install = true,

    highlight = {
        -- `false` will disable the whole extension
        enable = true,

        -- Setting this to true will run `:h syntax` and tree-sitter at the same time.
        -- Set this to `true` if you depend on 'syntax' being enabled (like for indentation).
        -- Using this option may slow down your editor, and you may see some duplicate highlights.
        -- Instead of true it can also be a list of languages
        additional_vim_regex_highlighting = false,
    },
    rainbow = {
        enable = true,
        -- Which query to use for finding delimiters
        query = {
            'rainbow-parens',
            'rainbow-blocks',
            'rainbow-tags',
        },
        -- Highlight the entire buffer all at once
        --strategy = rainbow.strategy.global,
        strategy = rainbow.strategy.locally,

        hlgroups = {
            'TSRainbowYellow',
            'TSRainbowMagenta',
            'TSRainbowBlue',
        },

    }
}

