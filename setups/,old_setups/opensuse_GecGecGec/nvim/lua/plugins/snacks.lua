return {
  "folke/snacks.nvim",
  opts = {
    scroll = {
      enabled = true,
      animate = {
        duration = { step = 15, total = 60 },
        easing = "linear",
      },
      -- faster animation when repeating scroll after delay
      animate_repeat = {
        delay = 25, -- delay in ms before using the repeat animation
        duration = { step = 3, total = 20 },
        easing = "linear",
      },
    },
  },
}
