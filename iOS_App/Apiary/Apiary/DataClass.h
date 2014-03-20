//
//  DataClass.h
//  Apiary
//
//  Created by John Davidge on 15/03/2014.
//  Copyright (c) 2014 John Davidge. All rights reserved.
//

#import <Foundation/Foundation.h>

@interface DataClass : NSObject {
    NSString *user;
    NSString *password;
    NSString *url;
    NSString *device_id;
    NSString *device_type;
    NSString *filePath;
    NSMutableDictionary *data_storage;
}
@property(nonatomic,retain)NSString *user;
@property(nonatomic,retain)NSString *password;
@property(nonatomic,retain)NSString *url;
@property(nonatomic,retain)NSString *device_id;
@property(nonatomic,retain)NSString *device_type;
@property(nonatomic,retain)NSString *filePath;
@property(nonatomic,retain)NSMutableDictionary *data_storage;
+(DataClass*)getInstance;
@end