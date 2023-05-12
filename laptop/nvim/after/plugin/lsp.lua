-- Learn the keybindings, see :help lsp-zero-keybindings
-- Learn to configure LSP servers, see :help lsp-zero-api-showcase
local lsp = require('lsp-zero')
lsp.preset('recommended')

lsp.ensure_installed({
	'tsserver',
	'eslint',
	--'sumneko_lua',
	'rust_analyzer',
	'pyright',
	'hls',
	'gopls',
})

-- When you don't have mason.nvim installed
-- You'll need to list the servers installed in your system
--lsp.setup_servers({'tsserver', 'eslint'})

-- (Optional) Configure lua language server for neovim
lsp.nvim_workspace()

--lsp.set_preferences({
--    sign_icons = {}
--})

--set completeopt=menu,menuone,noselect

local cmp = require('cmp')
--local cmp_select = {behavior = cmp.SelectBehavior.Select}
cmp.setup {
    confirmation = {
        --completeopt = 'menu,menuone,noselect,noinsert',
        --autocomplete = false,
        --select = false
    },
}
cmp.preselect = false
local cmp_mappings = lsp.defaults.cmp_mappings({
	--['<C-p>'] = cmp.mapping.select_prev_item(cmp_select),
	--['<C-n>'] = cmp.mapping.select_next_item(cmp_select),
    --['<Tab>'] = cmp.mapping.confirm({select = false}),
	--['<C-Space>'] = cmp.mapping.complete(),
    --['Enter'] = fallback(),
    --['<CR>'] = cmp.mapping.confirm({ select = false }),
    --['<CR>'] = cmp.mapping.close(),
    ['<Tab>'] = cmp.mapping.confirm(),
    ['<C-i>'] = cmp.mapping.close(),
    ['<CR>'] = cmp.mapping(function(fallback)
        fallback()
    end)

})
lsp.setup_nvim_cmp({
	mapping = cmp_mappings
})

lsp.on_attach(function(client, bufnr)
	local opts = {buffer = bufnr, remap = false}

	vim.keymap.set("n", "gd", function() vim.lsp.buf.definition() end, opts)
	vim.keymap.set("n", "K", function() vim.lsp.buf.hover() end, opts)
	--vim.keymap.set("n", "<leader>vk", function() vim.diagnostic.open_float() end, opts)
	vim.keymap.set("n", "N", function() vim.diagnostic.open_float() end, opts)
    vim.opt.signcolumn = "yes"
    client.server_capabilities.semanticTokensProvider = nil
end)

lsp.setup()
