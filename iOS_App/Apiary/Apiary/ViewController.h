//
//  ViewController.h
//  Apiary
//
//  Created by John Davidge on 15/03/2014.
//  Copyright (c) 2014 John Davidge. All rights reserved.
//

#import <UIKit/UIKit.h>

@interface ViewController : UIViewController{
    IBOutlet UITextField *usernameField;
    IBOutlet UITextField *passwordField;
}

- (IBAction)usernameFieldDismiss:(id)sender;
- (IBAction)passwordFieldDismiss:(id)sender;

@end
