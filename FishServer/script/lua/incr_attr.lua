local function to_number(val, dft)
    local v = tonumber(val)
    if v == nil then
        v = dft
    end
    return v
end

local function incr_hash_field(key, field, delta, mode, low, high)
    local cur = to_number(redis.call('HGET', key, field), 0)
    local final = cur
    local fixed = 0
    -- fix negative number
    if cur < 0 then
        fixed = -cur
        final = to_number(redis.call('HINCRBY', key, field, fixed), 0)
        cur = final
    end
    -- check low limit
    if low ~= -1 and cur < low then
        return { 0, final, fixed }
    end
    -- check high limit
    if high ~= -1 and cur > high then
        return { 0, final, fixed }
    end
    if delta >= 0 or cur + delta >= 0 then
        final = to_number(redis.call('HINCRBY', key, field, delta), 0)
        return { delta, final, fixed }
    end
    -- noop
    if mode == 0 or cur == 0 then
        return { 0, cur, fixed }
    end
    -- clear to zero
    final = to_number(redis.call('HINCRBY', key, field, -cur), 0)
    return { -cur, final, fixed }
end

local delta = to_number(KEYS[1], 0)
local low = to_number(KEYS[2], 0)
local high = to_number(KEYS[3], 0)
local mode = to_number(KEYS[4], 0)
local key = KEYS[5]
local field = KEYS[6]

local result = incr_hash_field(key, field, delta, mode, low, high)
if field == 'chip' or field == 'diamond' or field == 'coupon' then
    -- field fixed
    if result[3] > 0 then
        redis.call('HINCRBY', key, 'fixed_' .. field, result[3])
    end
    -- field incr
    if result[1] > 0 then
        redis.call('HINCRBY', key, 'in_' .. field, result[1])
    elseif result[1] < 0 then
        redis.call('HINCRBY', key, 'out_' .. field, -result[1])
    end
end
return result
