//
//  ApiaryViewController.m
//  Apiary
//
//  Created by John Davidge on 15/03/2014.
//  Copyright (c) 2014 John Davidge. All rights reserved.
//

#import "ApiaryViewController.h"
#import "DataClass.h"

@interface ApiaryViewController ()

@end

@implementation ApiaryViewController

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
    _webView.delegate = self;
    [_activityIndicator startAnimating];
    // Get an instance of DataClass
    DataClass *obj=[DataClass getInstance];
    obj.url = [obj.data_storage objectForKey:@"URL"];
    obj.user = [obj.data_storage objectForKey:@"username"];
    obj.password = [obj.data_storage objectForKey:@"password"];
    obj.device_id = [obj.data_storage objectForKey:@"device_id"];
    // Build the login URL
    NSString *fullURL = [obj.url stringByAppendingString:@"/login"];
    NSURL *url = [NSURL URLWithString:fullURL];
    // Debug output
    NSLog(@"URL: %@", fullURL);
    // Build POST body
    NSString *post = @"user=";
    post = [post stringByAppendingString:obj.user];
    post = [post stringByAppendingString:@"&password="];
    post = [post stringByAppendingString:obj.password];
    post = [post stringByAppendingString:@"&device_id="];
    post = [post stringByAppendingString:obj.device_id];
    post = [post stringByAppendingString:@"&device_name="];
    post = [post stringByAppendingString:@"iPhone"];
    NSData *postData = [post dataUsingEncoding:NSASCIIStringEncoding allowLossyConversion:YES];
    NSString *postLength = [NSString stringWithFormat:@"%d", [postData length]];
    // Initialise and config an HTTP request
    NSMutableURLRequest *request = [[NSMutableURLRequest alloc] init];
    [request setURL:url];
    [request setHTTPMethod:@"POST"];
    [request setValue:postLength forHTTPHeaderField:@"Content-Length"];
    [request setValue:@"application/x-www-form-urlencoded" forHTTPHeaderField:@"Content-Type"];
    // Set the request body
    [request setHTTPBody:postData];
    // Fire the HTTP request and load the result
    [_webView loadRequest:request];
}

- (void)webViewDidFinishLoad:(UIWebView *)webView
{
    [_activityIndicator stopAnimating];
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
