//
//  WebViewController.h
//  Apiary
//
//  Created by John Davidge on 10/25/13.
//  Copyright (c) 2013 John Davidge. All rights reserved.
//

#import <UIKit/UIKit.h>

@interface WebViewController : UIViewController {
    IBOutlet UITextField *hiveIPField;
}
- (IBAction)hiveIPFieldDismiss:(id)sender;
@property (weak, nonatomic) IBOutlet UIWebView *webView;


@end
