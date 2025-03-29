import os
from jupyter_core.paths import jupyter_data_dir

# Server configuration
c.ServerApp.ip = '0.0.0.0'
c.ServerApp.port = 8888
c.ServerApp.open_browser = False
c.ServerApp.token = os.environ.get('JUPYTER_TOKEN', 'your_jupyter_token')
c.ServerApp.allow_root = True

# Security
c.ServerApp.password = ''  # Disable password authentication
c.ServerApp.allow_origin = '*'
c.ServerApp.allow_credentials = True

# Resource limits
c.ServerApp.max_buffer_size = 1000000000  # 1GB
c.ServerApp.max_message_size = 1000000000  # 1GB

# Content security
c.ServerApp.tornado_settings = {
    'headers': {
        'Content-Security-Policy': "frame-ancestors 'self' *"
    }
}

# File handling
c.ServerApp.root_dir = '/home/jovyan/work'
c.ServerApp.notebook_dir = '/home/jovyan/work/notebooks'

# Extensions
c.ServerApp.nbserver_extensions = {
    'jupyterlab_git': True,
    'jupyterlab_lsp': True,
    'jupyterlab_code_formatter': True
}

# LSP settings
c.LanguageServerManager.language_servers = {
    'python': {
        'argv': ['python', '-m', 'pylsp'],
        'languages': ['python']
    }
}

# Code formatting
c.ServerApp.jpserver_extensions = {
    'jupyterlab_code_formatter': True
}

# Git integration
c.GitConfig.user_name = 'Oforha AI'
c.GitConfig.user_email = 'ai@oforha.ai'

# Memory management
c.ServerApp.max_buffer_size = 1000000000  # 1GB
c.ServerApp.max_message_size = 1000000000  # 1GB

# Performance
c.ServerApp.shutdown_no_activity_timeout = 3600  # 1 hour
c.ServerApp.kernel_timeout = 3600  # 1 hour

# Logging
c.ServerApp.log_level = 'INFO'
c.ServerApp.log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
c.ServerApp.log_file = '/home/jovyan/.jupyter/jupyter.log'

# Caching
c.ServerApp.cache_files = True
c.ServerApp.cache_files_limit = 1000

# Authentication
c.ServerApp.authenticate_prometheus = False
c.ServerApp.allow_remote_access = True

# WebSocket settings
c.ServerApp.websocket_compression_options = {}
c.ServerApp.websocket_max_message_size = 1000000000  # 1GB

# File system
c.ServerApp.contents_manager_class = 'jupyter_server.services.contents.filemanager.FileContentsManager'
c.FileContentsManager.root_dir = '/home/jovyan/work'
c.FileContentsManager.allow_hidden = True

# Terminal
c.ServerApp.terminals_enabled = True
c.ServerApp.terminals_available = True

# Kernel management
c.ServerApp.kernel_manager_class = 'jupyter_server.services.kernels.kernelmanager.AsyncMappingKernelManager'
c.AsyncMappingKernelManager.kernel_spec_manager_class = 'jupyter_server.services.kernels.specmanager.AsyncMappingKernelSpecManager'
c.AsyncMappingKernelManager.default_kernel_name = 'python3' 