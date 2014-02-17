//
//  WebViewController.h
//  Apiary
//
//  Created by John Davidge on 10/25/13.
//  Copyright (c) 2013 John Davidge. All rights reserved.
//

#import <UIKit/UIKit.h>

@interface WebViewController : UIViewController 
@property (weak, nonatomic) IBOutlet UIWebView *webView;
@property (strong, nonatomic) NSString *request_type;

@end
