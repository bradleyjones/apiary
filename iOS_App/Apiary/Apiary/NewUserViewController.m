//
//  NewUserViewController.m
//  Apiary
//
//  Created by John Davidge on 16/03/2014.
//  Copyright (c) 2014 John Davidge. All rights reserved.
//

#import "NewUserViewController.h"
#import "DataClass.h"

@interface NewUserViewController ()

@end

@implementation NewUserViewController

- (id)initWithNibName:(NSString *)nibNameOrNil bundle:(NSBundle *)nibBundleOrNil
{
    self = [super initWithNibName:nibNameOrNil bundle:nibBundleOrNil];
    if (self) {
        // Custom initialization
    }
    return self;
}

- (void)viewDidLoad
{
    [super viewDidLoad];
    // Build the New User URL
    DataClass *obj=[DataClass getInstance];
    NSString *fullURL = [obj.url stringByAppendingString:@"/newuser"];
    NSURL *url = [NSURL URLWithString:fullURL];
    // Build the HTTP request
    NSMutableURLRequest *request = [[NSMutableURLRequest alloc] init];
    [request setURL:url];
    [request setHTTPMethod:@"POST"];
    // Make the HTTP request and load the result
    [_webView loadRequest:request];
}

- (void)didReceiveMemoryWarning
{
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

/*
#pragma mark - Navigation

// In a storyboard-based application, you will often want to do a little preparation before navigation
- (void)prepareForSegue:(UIStoryboardSegue *)segue sender:(id)sender
{
    // Get the new view controller using [segue destinationViewController].
    // Pass the selected object to the new view controller.
}
*/

@end
