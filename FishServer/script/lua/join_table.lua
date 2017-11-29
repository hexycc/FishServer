-- KEYS: [userId, gameId, roomId, tableId, total, [play_mode]]
-- ARGV: []
--  ACK: [seatid, before_cnt, after_cnt]

local function get_attrs(total)
    local attrs = {}
    for i = 1, total do
        table.insert(attrs, 'seat'..tostring(i-1))
    end
    return attrs
end

local function sit_down(uid, key, total)
    local attrs = get_attrs(total)
    local res = redis.call('HMGET', key, unpack(attrs))
    local sid = -1
    for i = 1, total do
        if res[i] == tostring(uid) then
            sid = i - 1
            return sid
        end
    end
    for i = 1, total do
        if tonumber(res[i]) <= 0 then
            sid = i - 1
            local field = 'seat' .. tostring(sid)
            redis.call('HSET', key, field, tostring(uid))
            break
        end
    end
    return sid
end

local function get_player_count(key, total)
    local attrs = get_attrs(total)
    local res = redis.call('HMGET', key, unpack(attrs))
    local cnt = 0
    for i = 1, total do
        if res[i] and tonumber(res[i]) > 0 then
            cnt = cnt + 1
        end
    end
    return cnt
end

local function join_table(uid, gid, rid, tid, total, mode)
    local key = 'table:' .. gid .. ':' .. tid
    local before_cnt = get_player_count(key, total)
    local seatid = sit_down(uid, key, total)

    local before_key = 'quick:' .. gid .. ':0'
    if before_cnt ~= 0 then
        if mode ~= nil then
            before_key = 'quick:' .. gid .. ':' .. rid .. ':' .. tostring(before_cnt) .. ':' .. mode
        else
            before_key = 'quick:' .. gid .. ':' .. rid .. ':' .. tostring(before_cnt)
        end
    end

    local after_cnt = get_player_count(key, total)
    local after_key = 'quick:' .. gid .. ':0'
    if after_cnt ~= 0 then
        if mode ~= nil then
            after_key = 'quick:' .. gid .. ':' .. rid .. ':' .. tostring(after_cnt) .. ':' .. mode
        else
            after_key = 'quick:' .. gid .. ':' .. rid .. ':' .. tostring(after_cnt)
        end
    end

    if before_cnt ~= after_cnt then
        redis.call('LREM', before_key, '0', tid)
        redis.call('RPUSH', after_key, tid)
    end

    return { seatid, before_cnt, after_cnt }
end

return join_table(KEYS[1], KEYS[2], KEYS[3], KEYS[4], tonumber(KEYS[5]), KEYS[6])
