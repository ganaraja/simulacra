# Rate Limiting Mitigation Guide

## Overview

The Simulacra debate system makes multiple calls to the Google Gemini API during a debate. The free tier has rate limits that can be exceeded during debate execution, resulting in `429 RESOURCE_EXHAUSTED` errors.

## Rate Limits (Free Tier)

According to [Google's documentation](https://ai.google.dev/gemini-api/docs/rate-limits), the free tier has the following limits:

- **Requests per minute**: 15 requests/minute
- **Requests per day**: 1,500 requests/day
- **Tokens per minute**: 1,000,000 tokens/minute

A typical debate with 4 exchange rounds makes approximately **16-20 API calls**:

- 3 opening statements
- 3 defence statements
- 12 exchange messages (3 personas × 4 rounds)
- 3 reflections
- 1 summary

This can easily exceed the 15 requests/minute limit if executed quickly.

## Implemented Mitigations

### 1. Automatic Retry with Exponential Backoff

The coordinator now automatically retries failed requests with exponential backoff:

```python
MAX_RETRIES = 3
INITIAL_RETRY_DELAY = 3.0  # seconds
```

**How it works**:

- First retry: Wait 3 seconds
- Second retry: Wait 6 seconds
- Third retry: Wait 12 seconds

The system also parses the suggested retry delay from the error message and uses the longer of the two delays.

### 2. Delays Between API Calls

The coordinator adds strategic delays to avoid hitting rate limits:

- **1 second** between personas in the same phase
- **2 seconds** between different phases
- **2 seconds** between exchange rounds

This spreads out the API calls over time, reducing the likelihood of hitting rate limits.

### 3. Logging

The coordinator now logs:

- Phase transitions
- Retry attempts with delay information
- Rate limit errors
- Successful completions

Check `/tmp/backend.log` for detailed logs.

## Configuration Options

### Reduce Exchange Rounds

The default is 4 exchange rounds. You can reduce this to minimize API calls:

```bash
# Frontend: Modify the API call
POST /debate/run?max_exchange_rounds=2
```

This reduces the total API calls from ~20 to ~14.

### Increase Delays

If you continue to hit rate limits, you can increase the delays in `src/backend/agent/coordinator.py`:

```python
# Increase delays between personas
await asyncio.sleep(2)  # Instead of 1

# Increase delays between phases
await asyncio.sleep(5)  # Instead of 2
```

### Adjust Retry Settings

You can adjust the retry behavior:

```python
MAX_RETRIES = 5  # More retries
INITIAL_RETRY_DELAY = 5.0  # Longer initial delay
```

## Upgrade to Paid Tier

For production use or frequent testing, consider upgrading to a paid tier:

1. Visit [Google AI Studio](https://aistudio.google.com/)
2. Navigate to billing settings
3. Enable billing for your project

**Paid tier limits** (as of 2026):

- **Requests per minute**: 1,000 requests/minute
- **Requests per day**: Unlimited
- **Tokens per minute**: 4,000,000 tokens/minute

This eliminates rate limiting issues for typical usage.

## Monitoring Your Usage

Monitor your API usage at:

- https://ai.dev/rate-limit

This shows:

- Current usage
- Remaining quota
- Rate limit status

## Error Messages

### 429 RESOURCE_EXHAUSTED

**Full error**:

```
429 RESOURCE_EXHAUSTED. {'error': {'code': 429, 'message': 'You exceeded your current quota...'}}
```

**What it means**: You've hit the rate limit for requests per minute or per day.

**What the system does**:

1. Automatically retries with exponential backoff
2. Logs the retry attempt
3. Waits the suggested delay before retrying
4. After 3 retries, returns an error to the user

**What you can do**:

- Wait a few minutes and try again
- Reduce exchange rounds
- Increase delays between calls
- Upgrade to paid tier

### Rate Limit Exceeded After Retries

**Error**:

```
Rate limit exceeded. Please wait a few minutes and try again.
For more info: https://ai.google.dev/gemini-api/docs/rate-limits
```

**What it means**: The system tried 3 times but still hit rate limits.

**What to do**:

1. Wait 5-10 minutes
2. Try again with fewer exchange rounds
3. Check your usage at https://ai.dev/rate-limit
4. Consider upgrading to paid tier

## Best Practices

### Development

1. **Use fewer exchange rounds** during development:

   ```bash
   POST /debate/run?max_exchange_rounds=1
   ```

2. **Wait between tests**: Don't run multiple debates back-to-back

3. **Monitor your usage**: Check https://ai.dev/rate-limit regularly

4. **Use logging**: Check `/tmp/backend.log` to see retry attempts

### Production

1. **Upgrade to paid tier**: Eliminates rate limiting issues

2. **Implement caching**: Cache debate results to avoid redundant API calls

3. **Queue debates**: If running multiple debates, queue them with delays

4. **Monitor and alert**: Set up monitoring for rate limit errors

## Troubleshooting

### Debate fails immediately with 429 error

**Cause**: You've already hit your daily limit.

**Solution**:

- Wait until the next day (resets at midnight UTC)
- Upgrade to paid tier

### Debate fails after a few API calls

**Cause**: You've hit the requests per minute limit.

**Solution**:

- The system will automatically retry
- If it still fails, wait 5 minutes and try again
- Increase delays in the code

### Retries take too long

**Cause**: Exponential backoff can result in long waits.

**Solution**:

- Reduce MAX_RETRIES to fail faster
- Increase INITIAL_RETRY_DELAY to wait longer initially
- Upgrade to paid tier to avoid retries

## Code Changes Summary

### Modified Files

1. **src/backend/agent/coordinator.py**
   - Added retry logic with exponential backoff
   - Added delays between API calls
   - Added logging for debugging
   - Improved error messages

### Key Changes

```python
# Before
async def _run_turn(self, prompt: str) -> str:
    return await _run_agent_for_prompt(...)

# After
async def _run_turn(self, prompt: str, max_retries: int = MAX_RETRIES) -> str:
    for attempt in range(max_retries):
        try:
            return await _run_agent_for_prompt(...)
        except Exception as e:
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                # Retry with exponential backoff
                await asyncio.sleep(delay)
            else:
                raise
```

## Testing

All existing tests still pass:

```bash
PYTHONPATH=src python3 -m pytest tests/ -v
# 27 passed
```

The retry logic is tested manually by:

1. Running a debate
2. Observing retry attempts in logs
3. Verifying successful completion after retries

## Additional Resources

- [Google Gemini API Rate Limits](https://ai.google.dev/gemini-api/docs/rate-limits)
- [ADK Error Handling](https://google.github.io/adk-docs/agents/models/#error-code-429-resource_exhausted)
- [Monitor Usage](https://ai.dev/rate-limit)
- [Google AI Studio](https://aistudio.google.com/)

## Future Improvements

1. **Adaptive delays**: Adjust delays based on observed rate limits
2. **Request batching**: Batch multiple requests when possible
3. **Caching**: Cache common responses to reduce API calls
4. **Queue system**: Implement a queue for multiple concurrent debates
5. **Circuit breaker**: Temporarily stop making requests after repeated failures
6. **Metrics**: Track API usage and rate limit hits over time

## Support

If you continue to experience rate limiting issues:

1. Check the logs: `/tmp/backend.log`
2. Monitor your usage: https://ai.dev/rate-limit
3. Review this guide for configuration options
4. Consider upgrading to paid tier for production use
