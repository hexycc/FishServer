-- KEYS: [userId, gameId, expire_at, total_time, [reward, ...]]
-- ARGV: []
--  ACK: [which_times, reward, final_chip]

local function issue_benefit(KEYS)
    local userId, gameId = KEYS[1], KEYS[2]
    local expire_at, total_times = tonumber(KEYS[3]), tonumber(KEYS[4])
    local rewards = {}
    for i = 1, total_times do
        table.insert(rewards, tonumber(KEYS[4+i]))
    end
    local daily_key = 'daily:' .. gameId .. ':' .. userId
    local res = redis.call('hmget', daily_key, 'expire_ts', 'benefit_times')
    local redis_expire_ts, redis_which_times = res[1], res[2]
    -- not exist
    if not redis_expire_ts then
        redis.call('hmset', daily_key, 'expire_ts', expire_at, 'benefit_times', 1)
        redis.call('expireat', daily_key, expire_at)
        redis_which_times = 1
    elseif tonumber(redis_expire_ts) >= expire_at then
        -- no time left
        if redis_which_times and tonumber(redis_which_times) >= total_times then
            return { -1, 0, 0 }
        end
        redis_which_times = redis.call('hincrby', daily_key, 'benefit_times', 1)
    else
        -- expired
        redis.call('del', daily_key)
        redis.call('hmset', daily_key, 'expire_ts', expire_at, 'benefit_times', 1)
        redis.call('expireat', daily_key, expire_at)
        redis_which_times = 1
    end

    local final_chip = redis.call('hincrby', 'game:' .. gameId .. ':' .. userId, 'chip', rewards[redis_which_times])
    return { redis_which_times, rewards[redis_which_times], final_chip }
end

return issue_benefit(KEYS)
