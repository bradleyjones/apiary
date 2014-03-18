//
//  SettingsViewController.h
//  Apiary
//
//  Created by John Davidge on 15/03/2014.
//  Copyright (c) 2014 John Davidge. All rights reserved.
//

#import <UIKit/UIKit.h>

@interface SettingsViewController : UIViewController{
    IBOutlet UITextField *hiveURLField;
}

- (IBAction)hiveURLFieldDismiss:(id)sender;

@end
