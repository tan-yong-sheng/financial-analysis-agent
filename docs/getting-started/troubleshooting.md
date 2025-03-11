# Troubleshooting Guide

Common issues and their solutions when using the Financial Analysis Agent.

## API Issues

### OpenAI API

1. **Authentication Error**
   ```
   Error: Invalid API key
   ```
   - Check that your API key is correctly set in `.env`
   - Verify the key is valid in OpenAI dashboard

2. **Rate Limits**
   ```
   Error: Rate limit exceeded
   ```
   - Implement exponential backoff
   - Consider upgrading API tier

### Financial Data API

1. **No Data Found**
   ```
   Error: No company profile found for {ticker}
   ```
   - Verify ticker symbol is correct
   - Check if company is supported by FMP

2. **API Connection Issues**
   ```
   Error: Failed to fetch financial data
   ```
   - Check internet connection
   - Verify API endpoint is accessible

## Installation Issues

1. **Dependency Conflicts**
   ```
   ERROR: pip's dependency resolver...
   ```
   Solution:
   ```bash
   pip install -r requirements.txt --no-deps
   pip install -r requirements.txt
   ```

2. **Python Version**
   ```
   SyntaxError: invalid syntax
   ```
   - Ensure Python 3.8+ is installed
   - Check virtual environment activation

## Usage Issues

1. **Memory Errors**
   ```
   MemoryError: Unable to allocate...
   ```
   - Reduce batch size in configuration
   - Increase system memory

2. **Timeout Errors**
   ```
   Error: Request timed out
   ```
   - Check network connection
   - Increase timeout settings

## Getting Help

If you're still experiencing issues:

1. Check the [GitHub Issues](https://github.com/tan-yong-sheng/financial-analysis-agent/issues)
2. Join our [Discord Community](https://discord.gg/XXX)
3. Contact support at support@example.com
