"""
Configuration management with environment support and new v16.0 features
Supports: Trading params, Indicators, Scanner, ATR stops
"""
import json
import os
from dotenv import load_dotenv


class Config:
    """Configuration management with environment support"""
    
    def __init__(self, config_file: str = "config.json"):
        load_dotenv()
        
        self.config_file = config_file
        self.config = self._load_config()
    
    def _load_config(self) -> dict:
        """Load configuration from JSON file"""
        default_config = {
            "trading": {
                "slot_size": 18.0,
                "entry_threshold": 0.75,
                "drop_threshold": 0.65,
                "panic_stop": 2.0,
                "stop_loss_total": 12.0,
                "timeout_breakeven": 1200,
                "min_exchange_limit": 5.2,
                "volatility_min": 0.85,
                "spread_max": 0.10,
                "use_dynamic_stops": True,
                "atr_multiplier": 1.5,
                "min_stop_pct": 1.0
            },
            "symbols": ["NOT/USDT", "TON/USDT", "BNB/USDT", "SOL/USDT", "XRP/USDT", "ADA/USDT"],
            "exchange": {"name": "bybit"},
            "api_retry": {"max_retries": 3, "retry_delay": 0.5, "backoff_factor": 2.0},
            "cache": {"ticker_ttl": 2, "balance_ttl": 5, "ohlcv_ttl": 10},
            "indicators": {
                "enabled": True,
                "rsi_period": 14,
                "rsi_oversold": 30,
                "rsi_overbought": 70,
                "ema_fast": 9,
                "ema_slow": 21,
                "macd_fast": 12,
                "macd_slow": 26,
                "macd_signal": 9,
                "min_signal_score": 2
            },
            "stochastic": {
                "enabled": True,
                "period": 14,
                "k_smooth": 3,
                "d_smooth": 3
            },
            "scanner": {
                "enabled": True,
                "file": "hot_symbols.txt",
                "cache_ttl": 600,
                "use_priority": True
            }
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    loaded = json.load(f)
                    self._deep_merge(default_config, loaded)
            except Exception as e:
                print(f"Warning: Could not load config file: {e}")
        
        return default_config
    
    def _deep_merge(self, base: dict, updates: dict) -> None:
        """Deep merge updates into base dict"""
        for key, value in updates.items():
            if isinstance(value, dict) and key in base and isinstance(base[key], dict):
                self._deep_merge(base[key], value)
            else:
                base[key] = value
    
    def get_trading_config(self) -> dict:
        """Get trading parameters"""
        return self.config['trading']
    
    def get_symbols(self) -> list:
        """Get trading symbols"""
        return self.config['symbols']
    
    def get_api_config(self) -> dict:
        """Get API configuration"""
        return {
            'apiKey': os.getenv('BYBIT_API_KEY', ''),
            'secret': os.getenv('BYBIT_API_SECRET', ''),
            'enableRateLimit': True,
            'options': {
                'defaultType': 'spot',
                'recvWindow': 10000
            }
        }
    
    def get_retry_config(self) -> dict:
        """Get retry configuration"""
        return self.config['api_retry']
    
    def get_cache_config(self) -> dict:
        """Get cache configuration"""
        return self.config['cache']
    
    def get_indicator_config(self) -> dict:
        """Get technical indicators configuration"""
        return self.config.get('indicators', {
            "enabled": True,
            "rsi_period": 14,
            "rsi_oversold": 30,
            "rsi_overbought": 70,
            "ema_fast": 9,
            "ema_slow": 21,
            "macd_fast": 12,
            "macd_slow": 26,
            "macd_signal": 9,
            "min_signal_score": 2
        })
    
    def get_stochastic_config(self) -> dict:
        """Get Stochastic Oscillator configuration (NEW in v16.0)"""
        return self.config.get('stochastic', {
            "enabled": True,
            "period": 14,
            "k_smooth": 3,
            "d_smooth": 3
        })
    
    def get_scanner_config(self) -> dict:
        """Get Scanner configuration (NEW in v16.0)"""
        return self.config.get('scanner', {
            'enabled': True,
            'file': 'hot_symbols.txt',
            'cache_ttl': 600,
            'use_priority': True
        })
    
    def are_indicators_enabled(self) -> bool:
        """Check if technical indicators are enabled"""
        return self.get_indicator_config().get('enabled', True)
    
    def is_stochastic_enabled(self) -> bool:
        """Check if Stochastic is enabled (NEW in v16.0)"""
        return self.get_stochastic_config().get('enabled', True)
    
    def use_dynamic_stops(self) -> bool:
        """Check if dynamic ATR stops are enabled (NEW in v16.0)"""
        return self.get_trading_config().get('use_dynamic_stops', False)


# Global config instance
config = Config()
