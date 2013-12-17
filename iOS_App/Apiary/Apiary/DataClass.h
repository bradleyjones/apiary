//
//  DataClass.h
//  Apiary
//
//  Created by John Davidge on 12/16/13.
//  Copyright (c) 2013 John Davidge. All rights reserved.
//

#import <Foundation/Foundation.h>

@interface DataClass : NSObject {
    NSString *user;
    NSString *password;
    NSString *url;
    
}
@property(nonatomic,retain)NSString *user;
@property(nonatomic,retain)NSString *password;
@property(nonatomic,retain)NSString *url;
+(DataClass*)getInstance;
@end
