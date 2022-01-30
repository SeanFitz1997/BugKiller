from pynamodb.attributes import MapAttribute, UnicodeAttribute, UTCDateTimeAttribute


class BugResolutionMapAttribute(MapAttribute):
    resolver_id = UnicodeAttribute()
    resolved_on = UTCDateTimeAttribute()
