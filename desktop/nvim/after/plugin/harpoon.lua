local mark = require("harpoon.mark")
local ui = require("harpoon.ui")

vim.keymap.set("n", "<leader>m", mark.add_file)
vim.keymap.set("n", "<C-i>", ui.toggle_quick_menu)


--local harpoon = require("harpoon")
--
--harpoon:setup()
--
--vim.keymap.set("n", "<leader>m", function() harpoon:list():append() end)
--vim.keymap.set("n", "<C-i>", function() harpoon.ui:toggle_quick_menu(harpoon:list()) end)


