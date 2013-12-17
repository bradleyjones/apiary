//
//  DataClass.m
//  Apiary
//
//  Created by John Davidge on 12/16/13.
//  Copyright (c) 2013 John Davidge. All rights reserved.
//

#import "DataClass.h"

@implementation DataClass
@synthesize user;
@synthesize password;
@synthesize url;
static DataClass *instance =nil;
+(DataClass *)getInstance
{
    @synchronized(self)
    {
        if(instance==nil)
        {
            instance= [DataClass new];
        }
    }
    return instance;
}
@end
