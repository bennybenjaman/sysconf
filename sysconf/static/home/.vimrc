syntax on
filetype plugin on
filetype on
set encoding=utf-8
set nocompatible
set backspace=indent,eol,start
set autoread
set tabstop=4                " Tabs are 4 spaces
set shiftwidth=4             " Indent is 4 spaces
set softtabstop=4
set expandtab                " use spaces instead of tabs
set smarttab                 " Tab goes to the next tab stop
set nofoldenable
set hlsearch                 " highlight matches
set ignorecase               " ignore case when searching (see smartcase)
set laststatus=2             " always display status line at the bottom
set noerrorbells
set vb t_vb=
set listchars=tab:>·,trail:·
set history=1000              " remember 1000 cmds
set nobackup                  " Don't make a backup before overwriting a file.
set nowritebackup             " And again.
set directory=/tmp            " Keep swap files in one location
set noswapfile                " no swap file
"set formatoptions+=r          " auto-format comments while typing
set wildmode=longest,list,full
set ruler
"set number                    " show line numbers column
autocmd BufWritePre * :%s/\s\+$//e  " remove trailing spaces on save
:map <F12> <C-PageDown>
:imap <F12> <C-PageDown>
inoremap <M-Space> <C-X><C-N>
inoremap <M-S-Space> <C-X><C-O>

" remember cursor position after close
if has("autocmd")
  au BufReadPost * if line("'\"") > 1 && line("'\"") <= line("$") | exe "normal! g'\"" | endif
endif

" keep visual selection
vnoremap < <gv
vnoremap > >gv
