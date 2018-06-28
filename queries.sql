SELECT DATE_FORMAT(B.writeDate, "%M %d %Y %r") as wDate, B.id, DISTINCT B.ip, B.type FROM ( select id, max(writeDate) writeDate from dc1 group by id ) A INNER JOIN dc1 B USING (id,writeDate) WHERE B.writeDate <= DATE_SUB(NOW(), INTERVAL 2 HOUR) AND B.writeDate >= DATE_SUB(NOW(), INTERVAL 2 DAY) AND id != '' AND id != 'None'



SELECT id, MAX(writeDate)
FROM dc1
WHERE id != '' AND id != 'None'
GROUP BY id
ORDER BY MAX(writeDate) DESC

SELECT id, ip, MAX(writeDate)
FROM dc1
WHERE id != '' AND id != 'None'
GROUP BY id, ip