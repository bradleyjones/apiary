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
@synthesize filePath;
@synthesize data_storage;
static DataClass *instance =nil;
+(DataClass *)getInstance
{
    @synchronized(self)
    {
        if(instance==nil)
        {
            instance= [DataClass new];
            
            NSArray *directories = NSSearchPathForDirectoriesInDomains(NSDocumentDirectory, NSUserDomainMask, YES);
            NSString *documents = [directories lastObject];
            instance.filePath = [documents stringByAppendingPathComponent:@"data_storage.plist"];
            instance.data_storage = [NSMutableDictionary dictionaryWithObjectsAndKeys:@"URL", @"", @"username", @"", @"password", @"", nil];
            [instance.data_storage writeToFile:instance.filePath atomically:YES];
        }
    }
    return instance;
}
@end
