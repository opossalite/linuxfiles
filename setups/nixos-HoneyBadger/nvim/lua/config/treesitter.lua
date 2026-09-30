-- Neovim 0.12+ ships Tree-sitter parser installation, highlighting, and
-- indentation natively -- no plugin needed. (nvim-treesitter was archived in
-- April 2026 once this landed in core; its rewritten "main" branch also
-- requires a separate tree-sitter-cli binary just to build parsers, which
-- native installation does not.)

if vim.fn.has("nvim-0.12") == 0 then
  vim.notify(
    "Neovim 0.12+ is required for native Tree-sitter parser installation. "
      .. "Syntax highlighting/indent will fall back to Vim's regex-based "
      .. "defaults until you upgrade.",
    vim.log.levels.WARN
  )
  return
end

local ensure_installed = {
  "lua", "vim", "vimdoc", "query",
  "bash",
  "python",
  "javascript", "typescript", "tsx",
  "rust",
  "go", "gomod", "gowork", "gosum",
  "c", "cpp",
  "json", "yaml", "toml", "markdown", "markdown_inline",
}

-- vim.treesitter.language.add loads a parser, which only succeeds if it's
-- already installed -- so it doubles as an "is this installed?" check.
local function is_installed(lang)
  return pcall(vim.treesitter.language.add, lang)
end

-- Install anything from the list above that's missing. Only needs curl, tar,
-- and a C compiler (cc/gcc/clang) on PATH -- no tree-sitter CLI required.
for _, lang in ipairs(ensure_installed) do
  if not is_installed(lang) then
    pcall(vim.treesitter.language.install, lang)
  end
end

-- Enable highlighting + treesitter-based indent per buffer. This also
-- auto-installs the parser the first time you open a filetype that wasn't in
-- the list above ("syntax highlighting" + "proper tabbing").
vim.api.nvim_create_autocmd("FileType", {
  group = vim.api.nvim_create_augroup("UserTreesitter", { clear = true }),
  callback = function(event)
    local lang = vim.treesitter.language.get_lang(event.match) or event.match

    local function enable()
      if pcall(vim.treesitter.start, event.buf, lang) then
        vim.bo[event.buf].indentexpr = "v:lua.vim.treesitter.indentexpr()"
      end
    end

    if is_installed(lang) then
      enable()
    elseif pcall(vim.treesitter.language.install, lang) then
      enable()
    end
    -- If installation fails (unknown language, no network, no compiler),
    -- the buffer just falls back to Vim's regex syntax highlighting.
  end,
})
